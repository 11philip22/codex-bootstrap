# Codex sanndbox PC bootstrap

## Requirements

- Debian or Ubuntu on x86-64 or ARM64, booted with systemd, with Node.js 16 or newer available from the distribution's repositories.
- Root access and an internet connection to GitHub and the package repositories.
- A GitHub account with at least one public SSH authentication key you want to authorize for `codex`.
- For first-time Codex login, a browser and a ChatGPT account with device code login enabled. If needed, enable it in your ChatGPT security settings or ask your workspace admin to enable it.
- For the optional Deskflow playbook, an existing `codex` account, an XFCE desktop, and the `deskflow` package in your configured repositories.

## Run

On the Debian machine, log in as `root` or open a root shell with `su -`. If your account already has sudo access, you can use `sudo -i`.

```sh
apt-get update
apt-get install -y ca-certificates git ansible python3-apt

git clone https://github.com/11philip22/codex-bootstrap.git
cd codex-bootstrap
ansible-playbook bootstrap.yml
```

On the first run, enter the GitHub username, then enter and confirm the shared Linux and Samba password for `codex`. Password input is hidden. Machines set up with an older version prompt once on upgrade.

Later runs use the saved GitHub username to add new public SSH keys and keep the existing passwords. Removing a key on GitHub does not revoke it on this machine. To set a new shared password, supply `codex_password` in an Ansible Vault file with `ansible-playbook bootstrap.yml -e @secrets.yml --ask-vault-pass`.

If the `codex` user is signed out, the playbook prints a URL and a one-time code. Open the URL in your browser and enter the code. The playbook waits for approval, then starts or restarts the service. Subsequent runs skip login while the user is signed in.

To install Deskflow separately and start it whenever `codex` logs in to XFCE, run the optional playbook from the repository directory.

```sh
ansible-playbook deskflow.yml
```
