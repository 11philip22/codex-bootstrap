#!/bin/bash
set -eu
cd "$(dirname "$0")/.."

declare -A settings
dpkg-query() { printf '%s\n' "$package_version"; }
xfconf-query() {
    [[ $1 == -c && $2 == xfce4-power-manager && $3 == -p ]] || return 2
    if (( $# == 4 )); then
        [[ -v settings[$4] ]] || return 1
        printf '%s\n' "${settings[$4]}"
    else
        [[ $# == 9 && $5 == --create && $6 == -t && $7 == uint && $8 == -s ]] || return 2
        settings[$4]=$9
        writes=$((writes + 1))
    fi
}

for package_version in 4.18.3-1 4.20.0-1; do
    settings=()
    writes=0
    source files/xfce/set-idle-power.sh
    expected=0
    if [[ $package_version == 4.18.* ]]; then expected=14; fi
    for power in ac battery; do
        [[ ${settings[/xfce4-power-manager/inactivity-on-$power]} == "$expected" ]]
        [[ ${settings[/xfce4-power-manager/dpms-on-$power-sleep]} == 0 ]]
        [[ ${settings[/xfce4-power-manager/dpms-on-$power-off]} == 0 ]]
    done
    [[ $writes == 6 ]]
    source files/xfce/set-idle-power.sh
    [[ $writes == 6 ]]
    settings[/xfce4-power-manager/dpms-on-ac-off]=10
    source files/xfce/set-idle-power.sh
    [[ $writes == 7 && ${settings[/xfce4-power-manager/dpms-on-ac-off]} == 0 ]]
done
