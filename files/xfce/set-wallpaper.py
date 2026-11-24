#!/usr/bin/python3
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Xfconf", "0")
from gi.repository import Gdk, Xfconf


def main():
    wallpaper = "/usr/local/share/backgrounds/stars-space.jpg"
    Gdk.init([])
    screen = Gdk.Screen.get_default()
    Xfconf.init()
    try:
        desktop = Xfconf.Channel.get("xfce4-desktop")
        workspace = desktop.get_int("/backdrop/single-workspace-number", 0)
        for index in range(screen.get_n_monitors()):
            monitor = screen.get_monitor_plug_name(index) or str(index)
            backdrop = f"/backdrop/screen{screen.get_number()}/monitor{monitor}/workspace{workspace}"
            if desktop.get_bool(backdrop + "/backdrop-cycle-enable", False):
                desktop.set_bool(backdrop + "/backdrop-cycle-enable", False)
            if desktop.get_int(backdrop + "/image-style", 5) == 0:
                desktop.set_int(backdrop + "/image-style", 5)  # Zoom a previously hidden image.
            if desktop.get_string(backdrop + "/last-image", "") != wallpaper:
                desktop.set_string(backdrop + "/last-image", wallpaper)
        if not desktop.get_bool("/backdrop/single-workspace-mode", False):
            desktop.set_bool("/backdrop/single-workspace-mode", True)
    finally:
        Xfconf.shutdown()


if __name__ == "__main__":
    main()
