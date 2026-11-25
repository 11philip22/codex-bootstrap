# Playbook scope

`bootstrap.yml` and its imported task files own all package installation and all machine and user configuration outside the optional Deskflow boot sequence. This includes XFCE settings, inactivity behavior, and the manual i3lock button.

Limit `deskflow.yml` to LightDM automatic login and the startup of that session. After automatic login, launch Deskflow with the user's saved settings, then run i3lock. Start the XFCE desktop only after i3lock has acquired the lock.

# Host prerequisites

Target machines already have `sudo` installed. Keep it out of the bootstrap package list.

# README scope

Keep `README.md` limited to `Requirements` and `Run`. List prerequisites the operator must provide under `Requirements`. Put the commands and prompts needed to run the playbook under `Run`.

When adding a package or changing a task, edit the README only if the prerequisites or run instructions change. Omit installed-package lists, version checks, post-install verification, and tool usage examples unless the user explicitly requests them in the README.

# Idempotency

Every provisioning change must converge. A second run with identical inputs on an unchanged host must report `changed=0` and leave credentials, files, and running services alone. If managed state drifts, repair only what differs.

Prefer declarative modules. Guard imperative writes with a check of the actual managed state. Use `changed_when: false` only for read-only operations, never to hide a write. Test both an unchanged rerun and a run that repairs drift.
