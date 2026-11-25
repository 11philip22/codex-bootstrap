#!/bin/sh
set -eu

set_timeout() {
    property="/xfce4-power-manager/$1"
    if [ "$(xfconf-query -c xfce4-power-manager -p "$property" 2>/dev/null)" != "$2" ]; then
        xfconf-query -c xfce4-power-manager -p "$property" --create -t uint -s "$2"
    fi
}

version=$(dpkg-query -W -f='${Version}' xfce4-power-manager)
never=0
# Older XFCE power managers use 14 as the sentinel for "Never".
if dpkg --compare-versions "${version#*:}" lt 4.19.3; then
    never=14
fi

for source in ac battery; do
    set_timeout "inactivity-on-$source" "$never"
    set_timeout "dpms-on-$source-sleep" 0
    set_timeout "dpms-on-$source-off" 0
done
