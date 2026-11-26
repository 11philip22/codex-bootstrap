#!/bin/sh
set -eu

channel=xfce4-panel
icon=/usr/local/share/icons/codex-applications-pentagram.svg

xfconf-query -c "$channel" -lv |
    awk '$1 ~ /^\/plugins\/plugin-[0-9]+$/ && $2 == "applicationsmenu" {print $1}' |
    while IFS= read -r plugin; do
        property="$plugin/button-icon"
        current=$(xfconf-query -c "$channel" -p "$property" 2>/dev/null) || current=
        if [ "$current" != "$icon" ]; then
            xfconf-query -c "$channel" -p "$property" --create -t string -s "$icon"
        fi
    done
