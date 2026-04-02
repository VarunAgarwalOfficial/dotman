#!/usr/bin/env bash

WALLPAPERS_DIR="${HOME}/.config/wallpapers"
CURRENT_FILE="${WALLPAPERS_DIR}/.current"

if [ -f "$CURRENT_FILE" ]; then
    WALLPAPER=$(cat "$CURRENT_FILE")
    if [ -f "$WALLPAPER" ]; then
        # Wait for hyprpaper to be ready
        sleep 0.5
        hyprctl hyprpaper preload "${WALLPAPER}"
        for monitor in $(hyprctl monitors | grep "Monitor" | awk '{print $2}'); do
            hyprctl hyprpaper wallpaper ",${WALLPAPER}"
        done
    fi
fi
