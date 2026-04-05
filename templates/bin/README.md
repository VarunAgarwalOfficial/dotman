# Bin Scripts

My collection of scripts that get deployed to `~/.local/bin/`. These handle everything from screenshots to menus.

## Structure

```
~/.local/bin/
├── screenshot              # Screenshot tool
├── terminal-rain           # Matrix-style screensaver
├── lib/
│   ├── menu-common         # Shared fzf menu library
│   ├── footspawn           # Spawn foot terminal for interactive apps
│   ├── screensaver-launcher # Lock + terminal-rain
│   └── gtk-apply           # Apply GTK/Papirus theme
└── menu/
    ├── launcher           # Main menu hub (SUPER+SPACE)
    ├── app-launcher        # Browse and launch .desktop apps
    ├── powermenu           # Shutdown/reboot/sleep/logout
    ├── theme-switcher      # Pick and apply a dotman theme
    ├── wallpaper-picker    # Browse wallpapers by theme
    ├── clipboard           # Clipboard history
    ├── quicknotes          # Daily notes in ~/quicknotes
    ├── vim-notes           # Notes browser in ~/notes
    ├── bin-run             # Run scripts from ~/.local/bin
    ├── pkill               # Process killer
    ├── yay                 # Pacman/AUR wrapper
    └── yay                 # Pacman/AUR wrapper
```

## Keybindings

These are the main ways I access my scripts from Hyprland:

| Key | Action |
|-----|--------|
| `SUPER + SPACE` | Open launcher menu |
| `SUPER + ESC` | Lock screen (screensaver) |
| `SUPER + SHIFT + B` | bluetui (Bluetooth manager) |
| `SUPER + SHIFT + W` | impala (network manager) |
| `SUPER + SHIFT + V` | wiremix (volume mixer) |
| `SUPER + SHIFT + C` | btop (system monitor) |

## Waybar Integration

Clicking certain waybar modules opens these scripts:

| Module | Action |
|--------|--------|
| Bluetooth | footspawn bluetui |
| Pacman updates | footspawn yay |
| Network | footspawn impala |
| Audio | footspawn wiremix |
| Media (right-click) | footspawn cava |
| Weather | footspawn curl wttr.in |

## Menu Common

The `lib/menu-common` file is sourced by all menu scripts. It sets up fzf colors using my current dotman theme, so when I switch themes my menus automatically update.

The main function is `run_menu()` - give it a prompt and some items, it runs fzf and returns the selection.

## Footspawn

Foot terminal launcher. Most of my menus run inline, but when I need an interactive TUI session (like nvim or btop), I spawn a new foot window with this script. It sets FOOT_CLASS=floating so I can style these windows differently in Hyprland.
