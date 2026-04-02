# Themes

Themes define the colors and config settings that Dotman applies across all my apps.

## Creating a Theme

Create a new YAML file in `themes/`:

```yaml
colors:
  # Backgrounds
  bg0: "#1e1e2e"  # Darkest
  bg1: "#181825"  # Primary
  bg2: "#313244"  # Secondary
  bg3: "#45475a"  # Highlights

  # Foregrounds
  fg0: "#cdd6f4"  # Primary text
  fg1: "#a6adc8"  # Dimmed text

  # ANSI colors
  black:   "#11111b"
  red:     "#f38ba8"
  green:   "#a6e3a1"
  yellow:  "#f9e2af"
  blue:    "#89b4fa"
  magenta: "#cba6f7"
  cyan:    "#94e2d5"
  white:   "#bac2de"

  # Bright variants
  bright_black:   "#585b70"
  bright_red:     "#f38ba8"
  bright_green:   "#a6e3a1"
  bright_yellow:  "#f9e2af"
  bright_blue:    "#89b4fa"
  bright_magenta: "#cba6f7"
  bright_cyan:    "#94e2d5"
  bright_white:   "#a6adc8"

  # Main accent
  accent: "#f9e2af"

config:
  theme_name: catppuccin
  papirus_folder_color: yellow
```

## Required Variables

Every theme needs these colors:

- `bg0`, `bg1`, `bg2`, `bg3` - backgrounds
- `fg0`, `fg1` - foregrounds
- `black` through `white` - ANSI colors
- `bright_black` through `bright_white` - bright variants
- `accent` - main accent color

And these config values (defined in `config.yaml` and `apps.yaml`):

- `gap`, `padding`, `border_size`, `border_radius`
- `font_main`, `font_heading`, `font_emoji`, `font_icons`, `font_size`
- `timeout`, `shell`, `theme_name`
- `papirus_folder_color` (for icon theme)

Run `dotman validate <theme>` to check if a theme has all required values.

## Theme-Specific Options

| Variable | Description |
|----------|-------------|
| `theme_name` | Identifier for the theme |
| `papirus_folder_color` | Color for Papirus folders (red, green, yellow, blue, magenta, cyan) |
