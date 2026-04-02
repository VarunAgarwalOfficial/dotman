# Contributing

Hey, thanks for checking this out. Here's how to work with Dotman.

## Setup

Clone the repo:

```bash
git clone git@github.com:VarunAgarwalOfficial/dotman.git ~/dotman
cd ~/dotman
```

Install dependencies:

```bash
pip install pyyaml jinja2
```

## Adding a New Theme

1. Create `themes/<theme-name>.yaml`
2. Add all required colors (see `themes/README.md`)
3. Run `python3 dotman.py validate <theme-name>` to check for missing values
4. Test: `python3 dotman.py apply <theme-name> --dry-run`

## Adding a New App

1. Create a template folder in `templates/<app-name>/base/`
2. Add your config files with Jinja2 variables for colors
3. Register in `apps.yaml`:

```yaml
myapp:
  target: "~/.config/myapp"
  template: "templates/myapp"
  reload: "myapp --reload"
```

4. Test: `python3 dotman.py apply <theme> --only myapp --dry-run`

## Testing

Use `--dry-run` to preview changes without actually deploying anything:

```bash
./dotman.py apply catppuccin --dry-run
./dotman.py apply catppuccin --only hyprland --dry-run
```

Use `--verbose` to see what's happening:

```bash
./dotman.py apply catppuccin --verbose
```

Validate themes before applying:

```bash
./dotman.py validate catppuccin
```

## Code Style

- Keep the README tone friendly and conversational
- Scripts get their own folder under `templates/bin/`
- Use Jinja2 filters (`| hex`, `| strip`, `| rgb`, `| argb`) for color formatting
- Test reload commands work before committing

## Submitting Changes

1. Make your changes
2. Commit with a clear message
3. Push to your fork and open a PR

```bash
git add .
git commit -m "Add foo bar"
git push origin main
```
