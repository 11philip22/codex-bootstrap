# Codex sanndbox PC bootstrap

## Requirements

- Debian or Ubuntu on x86-64 or ARM64, booted with systemd, with Node.js 16 or newer available from the distribution's repositories.
- Root access and an internet connection to GitHub and the package repositories.
- A GitHub account with at least one public SSH authentication key you want to authorize for `codex`.

## Run

On the Debian machine, log in as `root` or open a root shell with `su -`. If your account already has sudo access, you can use `sudo -i`.

```sh
apt-get update
apt-get install -y ca-certificates git ansible python3-apt

git clone https://github.com/11philip22/codex-bootstrap.git
cd codex-bootstrap
ansible-playbook bootstrap.yml
```

Enter the GitHub username when prompted. The playbook adds all public SSH authentication keys from that account to `codex`. Removing a key on GitHub does not revoke it on this machine.

Enter and confirm the password for `codex` at the next prompt. Input is hidden. The playbook updates the Linux and Samba passwords independently when they differ from the password you entered.

For first-time setup, start ChatGPT device login as the `codex` service user from the same root shell.

```sh
su - codex -c 'codex login --device-auth'
```

Open the URL printed by Codex in your browser and enter the code. If device login is disabled, enable it in your ChatGPT security settings or ask your workspace admin to enable it.

After sign-in succeeds, restart the service to load the credentials.

```sh
systemctl restart codex.service
```
