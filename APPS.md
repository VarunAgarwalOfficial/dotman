# Apps

Apps that I manage with Dotman and the custom scripts I use every day.

## Apps I Manage

These are all the applications I configure through Dotman. Each one has a
template in `templates/` that gets rendered with my current theme colors.

- **hyprland** - My window manager
- **waybar** - Status bar
- **ghostty** - Terminal
- **fish** - Shell
- **bash** - Fallback shell
- **starship** - Prompt
- **fastfetch** - System info
- **btop** - System monitor
- **cava** - Audio visualizer
- **lazygit** - TUI git
- **bat** - Cat clone
- **foot** - Another terminal
- **mako** - Notifications
- **fontconfig** - Fonts
- **wallpapers** - Wallpapers
- **lazyvim** - Neovim config
- **opencode** - AI coding assistant
- **yazi** - File manager
- **bin** - My custom scripts

## Bin Scripts

All scripts deploy to `~/.local/bin/` with the following structure:

```
~/.local/bin/
├── screenshot              - Screenshot tool
├── terminal-rain           - ASCII rain screensaver
├── lib/
│   ├── menu-common         - Shared fzf menu library
│   ├── floating-terminal   - Floating foot terminal launcher
│   └── screensaver-launcher - Screensaver launcher with lock file
└── menu/
    ├── launcher           - Main menu hub (SUPER+SPACE)
    ├── app-launcher        - .desktop app browser
    ├── powermenu           - Shutdown/reboot/sleep/logout
    ├── theme-switcher      - Dotman theme switcher
    ├── wallpaper-picker    - Theme-based wallpaper selector
    ├── clipboard           - Clipboard history (text via cliphist)
    ├── quicknotes          - Daily notes in ~/quicknotes
    ├── vim-notes           - Notes browser in ~/notes
    ├── bin-run             - Run scripts from ~/.local/bin
    ├── pkill               - Process killer
    └── yay                 - Pacman/AUR package manager
```

### screenshot

I use grim for capturing and slurp for selection. Four modes:

- **Full screen** - captures the entire screen
- **Region** - select a region with slurp
- **Window** - shows visual window boxes, select one with slurp
- **Active window** - captures the currently focused window

After capture, optionally edits with swappy, then saves to ~/Screenshots.

### terminal-rain

ASCII rain screensaver. Matrix-like effect with occasional lightning strikes.
I run this in a fullscreen foot terminal when I'm away from my computer.

Originally inspired by https://github.com/rmaake1/terminal-rain-lightning

The rain is cyan characters falling down. Lightning is rarer and more dramatic,
with white bolts that branch and fork as they strike down, fading out after a bit.
ESC or Ctrl+C to exit, resizes automatically when the terminal changes size.

### launcher

Main menu hub. This pops up when I hit SUPER+SPACE. From here I can access
all my other menus and utilities without memorizing a bunch of keybinds.

The loop keeps showing the menu after each action so I can do multiple things
without reopening. ESC or empty selection exits.

### app-launcher

Browse and launch .desktop apps with fzf. Finds apps in
/usr/share/applications and ~/.local/share/applications, filters hidden ones.

### powermenu

Shutdown, reboot, sleep, or logout. I bound this to a key
so I can quickly power down or suspend when I'm done.

### theme-switcher

Pick a dotman theme and apply it. Runs in background so
the menu closes immediately. Sends a notification when done.

### wallpaper-picker

Browse by theme folder, then pick an image. Uses hyprpaper.
Saves the current choice so I can restore it later if needed.

### clipboard

Clipboard history. Uses cliphist with wl-clipboard to store and browse
clipboard history. Select an entry to restore it.

### quicknotes

I use this to jot down quick stuff without thinking too much.
Opens today's note file (2024-01-15.md) in nvim. Creates it with a header if
it doesn't exist yet.

### vim-notes

I keep all my notes in ~/notes and use this to browse and edit them.
Shows all my note files sorted by most recent, plus an option to create a new one.
Opens in nvim using my floating terminal.

### bin-run

I keep various helper scripts in ~/.local/bin and use this to
quickly run them without remembering where they are. Lists all executables
in the bin folder and runs the selected one.

### pkill

List running processes in fzf and kill the selected one.
Excludes fzf and foot since those are the menus themselves.

### yay

I use yay because it handles both official repos and the AUR.
Actions: search, search-installed, install, update, remove, clean.
Everything runs in a floating foot terminal.

### menu-common

Shared fzf menu library. All my menus source this file for consistent theming.
The FZF_DEFAULT_OPTS uses my dotman colors, so when I switch themes everything
updates automatically.

run_menu() is my main function. Give it a prompt and some items, it runs fzf
and returns the selection. go_back() exits with code 130 which parent menus
check for to return to the previous level.

### floating-terminal

I use foot as my terminal and sometimes need to
spawn floating windows for various things. This script handles that for me.

The FOOT_CLASS=floating sets an app-id so I can style these windows in Hyprland
(fullscreen, no borders, etc). Works with commands, stdin input, or interactive mode.

### screensaver-launcher

I call this from hypridle when I'm away for too long,
or manually with SUPER+Escape when I want to lock my screen.

Uses a lock file at /tmp/terminal-rain.lock so I don't end up running
multiple instances. The actual screensaver is terminal-rain running in
a fullscreen foot window.
