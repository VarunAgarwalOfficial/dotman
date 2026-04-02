# Source Code

The Python code that powers Dotman. Pretty small and straightforward.

## Files

- **dotman.py** - Entry point. Parses CLI args and calls the right command.

- **src/main.py** - CLI commands: `apply`, `list`, `validate`. Loads config, renders templates, handles backups.

- **src/config.py** - Loads YAML files (themes, apps, config). Validates required variables.

- **src/template.py** - Jinja2 rendering. Adds custom filters (`hex`, `strip`, `rgb`, `argb`) for color formatting.

- **src/deploy.py** - Backs up existing configs and writes new ones. Handles symlinks and creates directories.

## Running Tests

```bash
./dotman.py apply catppuccin --dry-run    # Preview what would happen
./dotman.py validate catppuccin            # Check theme is valid
```

## Adding a Command

1. Add the command function to `src/main.py`
2. Add the arg parser in `dotman.py`
3. Done.
