import subprocess

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    _supports_check_mode = False

    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp, task_vars)
        user = self._task.args["user"]
        login = ["sudo", "-n", "-i", "-u", user, "--", "/usr/local/bin/codex", "login"]

        status = subprocess.run([*login, "status"], capture_output=True, text=True)
        if status.returncode == 0:
            return dict(result, changed=False)
        if status.returncode != 1 or "Not logged in" not in status.stderr.splitlines():
            return dict(result, failed=True, msg=status.stderr.strip() or "Could not check Codex login status.")

        # Show the one-time code while Codex is waiting for browser approval.
        with subprocess.Popen(
            [*login, "--device-auth"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ) as process:
            for line in process.stdout:
                self._display.display(line.rstrip("\n"), screen_only=True)
            if process.wait() != 0:
                return dict(result, failed=True, msg="Codex device login failed. See the terminal output above.")

        return dict(result, changed=True)
