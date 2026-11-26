#!/bin/sh
set -eu

channel=xfce4-panel
panels=$(xfconf-query -c "$channel" -p /panels)
panel_ids=$(printf '%s\n' "$panels" | awk '/^[0-9]+$/')
removed=false

# XFCE's default bottom launcher panel uses the bottom-center position (10).
set --
for panel_id in $panel_ids; do
    position=$(xfconf-query -c "$channel" -p "/panels/panel-$panel_id/position")
    case "$position" in
        'p=10;'*) removed=true ;;
        *) set -- "$@" -t int -s "$panel_id" ;;
    esac
done

# Preserve the remaining panels and leave the launcher's settings available.
if [ "$removed" = true ] && [ "$#" -gt 0 ]; then
    xfconf-query -c "$channel" -p /panels --force-array "$@"
    xfce4-panel --restart
fi
