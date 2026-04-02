# Templates

Templates are where I store config files for each app. Dotman renders them through Jinja2 and deploys them to their target locations.

## Structure

Each app gets its own folder under `templates/`. Inside, there's a `base/` directory with the default config files. Optionally, I can add variant folders for different setups (like "dark" or "light").

```
templates/
├── hyprland/
│   └── base/
│       └── hyprland.conf
├── waybar/
│   ├── base/
│   │   └── config
│   └── dark/
│       └── config
└── ...
```

## How It Works

When I run `dotman apply catppuccin`:

1. Dotman loads the theme colors from `themes/catppuccin.yaml`
2. It renders each template through Jinja2, substituting `{{ color }}` variables
3. Backups the old config to `~/.local/state/dotman/backups/`
4. Deploys the new config to the target location
5. Runs the reload command if specified in apps.yaml

## Adding a New Template

1. Create a folder in `templates/` (e.g., `templates/myapp/`)
2. Add the config files using Jinja2 syntax for colors
3. Register the app in `apps.yaml`:

```yaml
myapp:
  target: "~/.config/myapp"
  template: "templates/myapp"
  reload: "myapp --reload"
```

## Template Variables

All templates have access to:

- **Colors**: `bg0`, `bg1`, `bg2`, `bg3`, `fg0`, `fg1`, `accent`, etc. (from theme YAML)
- **Config**: `gap`, `padding`, `border_size`, `font_main`, `font_size`, etc. (from config.yaml)
- **Filters**: `{{ accent | hex }}`, `{{ accent | strip }}`, `{{ accent | rgb }}`, `{{ accent | argb }}`

## Variants

Sometimes I want different configs for the same app. That's what variants are for. Pass `--appname variant` when applying:

```bash
./dotman.py apply catppuccin --waybar dark
```

Dotman will look for `templates/waybar/dark/` instead of `base/`.
