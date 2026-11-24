#!/usr/bin/python

import ctypes
import hmac
import os
import subprocess
from pathlib import Path

SHADOW = Path("/etc/shadow")
SMB_CONF = Path("/etc/samba/smb.conf")


def linux_password_matches(username, password):
    with SHADOW.open("rb") as shadow:
        prefix = username.encode() + b":"
        for entry in shadow:
            if entry.startswith(prefix):
                _, stored, _ = entry.split(b":", 2)
                break
        else:
            return False
    if not stored or stored.startswith((b"!", b"*")):
        return False

    crypt = ctypes.CDLL("libcrypt.so.1").crypt
    crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    crypt.restype = ctypes.c_char_p
    candidate = crypt(password.encode(), stored)
    if not candidate or candidate.startswith(b"*"):
        raise ValueError("Cannot verify the existing Linux password hash")
    return hmac.compare_digest(candidate, stored)


def samba_password_matches(username, password):
    from samba.credentials import Credentials
    from samba.samba3 import param, passdb

    params = param.get_context()
    params.load(str(SMB_CONF))
    # The managed standalone configuration uses tdbsam, which can create its DB on open.
    database_path = Path(params.get("private dir")) / "passdb.tdb"
    try:
        database_path.stat()
    except FileNotFoundError:
        return False

    database = passdb.PDB("tdbsam")
    if not any(entry["account_name"] == username for entry in database.search_users(0)):
        return False
    stored = database.getsampwnam(username).nt_passwd
    credentials = Credentials()
    credentials.set_password(password)
    return stored is not None and hmac.compare_digest(credentials.get_nt_hash(), stored)


def reconcile(module):
    username = module.params["username"]
    password = module.params["password"]
    if not username or username.startswith("-") or any(c in username for c in ":\r\n\0"):
        module.fail_json(msg="Invalid local username")
    if not password or any(c in password for c in "\r\n\0"):
        module.fail_json(msg="A nonempty single-line password is required")

    changed = False
    operation = "read the Linux password"
    try:
        linux_matches = linux_password_matches(username, password)
        operation = "read the Samba password"
        samba_matches = samba_password_matches(username, password)
        if module.check_mode:
            return not (linux_matches and samba_matches)

        if not linux_matches:
            operation = "set the Linux password"
            subprocess.run(
                ["/usr/sbin/chpasswd"],
                input=f"{username}:{password}\n".encode(),
                capture_output=True,
                check=True,
            )
            changed = True
        if not samba_matches:
            operation = "set the Samba password"
            subprocess.run(
                ["smbpasswd", "-s", "-a", username],
                input=f"{password}\n{password}\n".encode(),
                capture_output=True,
                check=True,
            )
            changed = True
    except Exception as error:
        # Backends may include credential data in diagnostics.
        module.fail_json(changed=changed, msg=f"Could not {operation} ({type(error).__name__})")
    return changed


def main():
    import fcntl
    from ansible.module_utils.basic import AnsibleModule

    module = AnsibleModule(
        argument_spec={
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
        },
        supports_check_mode=True,
    )
    # Serialize rotations across both stores, even when two local plays run together.
    try:
        lock = os.open(SMB_CONF.parent, os.O_RDONLY | os.O_DIRECTORY)
    except FileNotFoundError:
        if module.check_mode:
            module.exit_json(changed=True)
        module.fail_json(msg="The Samba configuration directory is missing")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX)
        changed = reconcile(module)
    finally:
        os.close(lock)
    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
