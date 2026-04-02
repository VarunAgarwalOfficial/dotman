#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$0")"
FZF_DRUN_CORE="$SCRIPT_DIR/fzf-drun.sh"

choice=$($FZF_DRUN_CORE theme-switcher powermenu app-launcher wallpaper-picker vim-notes clipboard quicknotes bin-run pkill)

case "$choice" in
    theme-switcher) "$SCRIPT_DIR/theme-switcher" ;;
    theme-wallpaper-picker) "$SCRIPT_DIR/theme-wallpaper-picker" ;;
    powermenu) "$SCRIPT_DIR/powermenu" ;;
    app-launcher) "$SCRIPT_DIR/app-launcher" ;;
    wallpaper-picker) "$SCRIPT_DIR/wallpaper-picker" ;;
    vim-notes) "$SCRIPT_DIR/vim-notes" ;;
    clipboard) "$SCRIPT_DIR/clipboard" ;;
    quicknotes) "$SCRIPT_DIR/quicknotes" ;;
    bin-run) "$SCRIPT_DIR/bin-run" ;;
    pkill) "$SCRIPT_DIR/pkill" ;;
esac
