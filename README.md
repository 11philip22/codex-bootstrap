# Codex sanndbox PC bootstrap

## Requirements

- Debian or Ubuntu on x86-64 or ARM64, booted with systemd, with Node.js 16 or newer available from the distribution's repositories.
- Root access and an internet connection to GitHub and the package repositories.

## Run

On the Debian machine, log in as `root` or open a root shell with `su -`. If your account already has sudo access, you can use `sudo -i`.

```sh
apt-get update
apt-get install -y ca-certificates git ansible-core python3-apt

git clone https://github.com/11philip22/codex-bootstrap.git
cd codex-bootstrap
ansible-playbook bootstrap.yml
```

From the same root shell, set the separate Samba password for `codex` to enable access to the `projects` share. Enter it twice when prompted on first-time setup.

```sh
smbpasswd -a codex
```

For first-time setup, start ChatGPT device login as the `codex` service user from the same root shell.

```sh
su - codex -c 'codex login --device-auth'
```

Open the URL printed by Codex in your browser and enter the code. If device login is disabled, enable it in your ChatGPT security settings or ask your workspace admin to enable it.

After sign-in succeeds, restart the service to load the credentials.

```sh
systemctl restart codex.service
```
