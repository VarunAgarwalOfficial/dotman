# Dotman

    ____        __                      
   / __ \____  / /_____ ___  ____ _____ 
  / / / / __ \/ __/ __ `__ \/ __ `/ __ \
 / /_/ / /_/ / /_/ / / / / / /_/ / / / /
/_____/\____/\__/_/ /_/ /_/\__,_/_/ /_/ 
                                        

Hey! This is my personal dotfile manager. I built this to keep all my configurations synchronized and themed across my system. Instead of manually updating configs for every application whenever I want to try a new color scheme, I just define my theme once and let Dotman handle the rest.

## What It Does

Dotman takes a theme file with all my colors and settings, renders it through Jinja2 templates for each application, backs up the old configs, and deploys the new ones. Simple as that. Change one file, update everything.

## Installation

You'll need Python 3.8 or later, plus PyYAML and Jinja2:

```bash
pip install pyyaml jinja2
chmod +x dotman.py
```

## Commands

Apply a theme to all my apps:

```bash
./dotman.py apply catppuccin
```

Preview changes without actually doing anything:

```bash
./dotman.py apply catppuccin --dry-run
```

Just want to update specific apps:

```bash
./dotman.py apply catppuccin --only hyprland,waybar
```

See what themes I have available:

```bash
./dotman.py list
```

Check if a theme has any issues:

```bash
./dotman.py validate
./dotman.py validate catppuccin
```

## Structure

```
dotman/
├── dotman.py              # Entry point
├── config.yaml            # Global settings
├── apps.yaml              # All the apps I manage
├── src/                   # Python code
│   ├── main.py            # CLI commands
│   ├── config.py          # YAML loading
│   ├── template.py        # Jinja2 rendering
│   └── deploy.py          # Backup & deploy
├── themes/                # My themes
│   ├── catppuccin.yaml
│   └── gruvbox-material.yaml
├── templates/             # Config templates per app
│   ├── hyprland/
│   ├── waybar/
│   ├── ghostty/
│   ├── fish/
│   └── ...
└── APPS.md                # Docs for apps & scripts I manage
```

## Configuration

### config.yaml

My global settings. The backup directory, defaults for spacing and fonts that I use across configs, etc.

```yaml
backup_dir: "~/.local/state/dotman/backups"
defaults:
  config:
    shell: fish
    gap: 4
    padding: 20
    border_size: 3
    border_radius: 0
    font_main: "JetBrains Mono"
    font_heading: "Iosevka"
    font_emoji: "OpenMoji Color"
    font_icons: "Font Awesome 7 Pro Mono"
    font_size: 16
    timeout: 5000
```

### apps.yaml

This is where I register all the applications I want themed. Each entry tells Dotman where the config goes, which template to use, and how to reload the app after deploying.

```yaml
required_config:
  - gap
  - padding
  - border_size
  - border_radius
  - font_main
  - font_heading
  - font_emoji
  - font_icons
  - font_size
  - timeout
  - shell

hyprland:
  target: "~/.config/hypr"
  template: "templates/hyprland"
  reload: "hyprctl reload"

waybar:
  target: "~/.config/waybar"
  template: "templates/waybar"
  reload: "killall waybar; waybar &"
```

The `required_config` list at the top is important. It defines which variables must be present in every theme. If a theme is missing something, Dotman will let me know.

## The Color System

I designed my themes to use a consistent set of 23 colors. This way, every template knows exactly what variables are available.

### Backgrounds

| Variable | Description |
|----------|-------------|
| `bg0` | Darkest background (desktop, deepest panels) |
| `bg1` | Primary background for windows |
| `bg2` | Secondary background (tooltips, elevated surfaces) |
| `bg3` | Lightest background, subtle highlights |

### Foregrounds

| Variable | Description |
|----------|-------------|
| `fg0` | Primary text, maximum contrast |
| `fg1` | Secondary or dimmed text |

### ANSI Colors

Standard terminal colors that I use throughout for status indicators, icons, and category highlights.

| Variable | My Typical Use |
|----------|----------------|
| `black` | Disabled, inactive |
| `red` | Errors, warnings |
| `green` | Success, active |
| `yellow` | Warnings, highlights |
| `blue` | Info, links |
| `magenta` | Special items |
| `cyan` | Connectivity, status |
| `white` | Subtle text |

### Bright Variants

Higher contrast versions of the ANSI colors.

| Variable |
|----------|
| `bright_black` through `bright_white` |

### Accent

The main accent color for focused elements and interactive components.

| Variable | Description |
|----------|-------------|
| `accent` | Primary accent color |

## Template Filters

Different apps want colors in different formats. Some need hex with `#`, others need RGB, and Hyprland uses ARGB. That's why I added these filters.

| Filter | Output | Example |
|--------|--------|---------|
| `hex` | Standard hex | `#89b4fa` |
| `strip` | Hex without hash | `89b4fa` |
| `rgb` | RGB values | `137, 180, 250` |
| `rgba(alpha)` | RGBA | `rgba(137, 180, 250, 0.5)` |
| `argb` | ARGB for Hyprland | `0xff89b4fa` |

Usage looks like this:

```conf
# Hyprland wants ARGB
col.active_border = {{ accent | argb }}

# Starship needs no hash
style = "{{ accent | strip }}"

# Waybar CSS uses hex
color: {{ accent }};
```

## Template Variables

Beyond colors, I can use config variables in templates too. Stuff like gaps, border sizes, fonts, and so on.

```css
/* Waybar */
window#waybar {
  border-radius: {{ border_radius }}px;
}
```

```conf
# Hyprland
general {
  gaps_in = {{ gap }}
  gaps_out = {{ gap * 2 }}
  border_size = {{ border_size }}
}
```

## Variants

Sometimes I want slightly different configs for the same app. That's what variants are for. I just pass `--appname variant` when applying:

```bash
./dotman.py apply catppuccin --hyprland dark
```

Dotman will look for `templates/hyprland/dark/` and use those files instead of base.

## Backups

Before touching anything, Dotman backs up my existing configs to `~/.local/state/dotman/backups/`. Backups are timestamped so I can always find a previous state. If I set `backup: false` in apps.yaml (like for wallpapers), it skips the backup.

## Adding New Apps

When I want to add a new app, I create a template directory with the config files using Jinja2 syntax, then add an entry to apps.yaml:

```yaml
myapp:
  target: "~/.config/myapp"
  template: "templates/myapp"
  reload: "myapp --reload"
```

## Tips

- Always run with `--dry-run` first to see what would change
- Use `--verbose` for detailed output
- Use `--only` to test on one app before rolling out everywhere
- Run `validate` before applying a new theme to catch missing colors early
