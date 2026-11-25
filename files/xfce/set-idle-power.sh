#!/bin/sh
set -eu

set_property() {
    if [ "$(xfconf-query -c "$1" -p "$2" 2>/dev/null)" != "$4" ]; then
        xfconf-query -c "$1" -p "$2" --create -t "$3" -s "$4"
    fi
}

set_property xfce4-screensaver /saver/idle-activation/enabled bool false

if [ -n "${DISPLAY:-}" ] && [ "${XDG_SESSION_TYPE:-x11}" = x11 ]; then
    display_settings=$(LC_ALL=C xset q)
    if ! printf '%s\n' "$display_settings" | grep -Eq '^[[:space:]]*timeout:[[:space:]]+0[[:space:]]'; then
        xset s off
    fi
fi

if ! command -v xfce4-power-manager >/dev/null; then
    exit 0
fi

version=$(dpkg-query -W -f='${Version}' xfce4-power-manager)
never=0
# Older XFCE power managers use 14 as the sentinel for "Never".
if dpkg --compare-versions "${version#*:}" lt 4.19.3; then
    never=14
fi

power=xfce4-power-manager
for source in ac battery; do
    set_property "$power" "/$power/inactivity-on-$source" uint "$never"
    set_property "$power" "/$power/dpms-on-$source-sleep" uint 0
    set_property "$power" "/$power/dpms-on-$source-off" uint 0
    if [ "$never" = 14 ]; then
        set_property "$power" "/$power/blank-on-$source" int 0
    fi
done
