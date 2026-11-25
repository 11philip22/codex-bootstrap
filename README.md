# Codex sanndbox PC bootstrap

## Requirements

- Debian or Ubuntu on x86-64 or ARM64, booted with systemd, with Node.js 16 or newer, `deskflow`, and `i3lock` available from the configured repositories.
- Root access and an internet connection to GitHub and the package repositories.
- A GitHub account with at least one public SSH authentication key you want to authorize for `codex`.
- For first-time Codex login, a browser and a ChatGPT account with device code login enabled. If needed, enable it in your ChatGPT security settings or ask your workspace admin to enable it.
- For automatic Deskflow startup, an XFCE X11 desktop using LightDM.

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

After bootstrap finishes, sign in to XFCE as `codex`, open Deskflow, and configure the connection to your other computer. Once the connection works, run the optional startup playbook from the repository directory in a root shell.

```sh
ansible-playbook deskflow.yml
```

On the next reboot, LightDM automatically logs in as `codex` and launches Deskflow with the user's saved settings. The session runs i3lock before opening the XFCE desktop. At the dark lock screen, type the `codex` password and press Enter to unlock.

To update a machine already using automatic Deskflow startup, run both playbooks from the updated checkout, then sign back into the Deskflow session.

```sh
ansible-playbook bootstrap.yml deskflow.yml
```
