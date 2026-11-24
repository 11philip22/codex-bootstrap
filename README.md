# Local Linux bootstrap

## Requirements

- Debian or Ubuntu on x86-64 or ARM64, with Node.js 16 or newer available from the distribution's repositories.
- A sudo-enabled account and an internet connection for package downloads.
- `ansible-core`. If needed, install it with `sudo apt-get update && sudo apt-get install ansible-core`.

## Run

Run this command from the cloned repository on the Linux machine.

```sh
ansible-playbook bootstrap.yml --ask-become-pass
```

Enter your sudo password at the `BECOME password` prompt.
