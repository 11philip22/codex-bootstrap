# Codex sanndbox PC bootstrap

## Requirements

- Debian or Ubuntu on x86-64 or ARM64, with Node.js 16 or newer available from the distribution's repositories.
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
