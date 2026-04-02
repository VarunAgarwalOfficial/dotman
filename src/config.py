"""Configuration loading and validation for Dotman."""

import os
import sys
import yaml
from pathlib import Path

# Required colors for all themes
REQUIRED_COLORS = {
    'bg0', 'bg1', 'bg2', 'bg3',
    'fg0', 'fg1',
    'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
    'bright_black', 'bright_red', 'bright_green', 'bright_yellow',
    'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white',
    'accent'
}


def get_dotman_dir() -> Path:
    """Get the dotman root directory based on script location."""
    # When running from src/, go up one level
    # When running from dotman.py, we're already at root
    script_dir = Path(__file__).parent
    
    # If we're in src/, go up to dotman root
    if script_dir.name == 'src':
        return script_dir.parent
    
    # Otherwise assume we're at dotman root
    return script_dir


DOTMAN_DIR = get_dotman_dir()


def load_yaml(path) -> dict:
    """Load a YAML file and return its contents."""
    path_str = str(path)
    if not os.path.exists(path_str):
        raise FileNotFoundError(f"Config file not found: {path_str}")

    with open(path_str, 'r') as f:
        data = yaml.safe_load(f)

    return data or {}


def load_config() -> dict:
    """Load the global config.yaml file."""
    config = load_yaml(DOTMAN_DIR / 'config.yaml')

    # Set defaults
    config.setdefault('backup_dir', '~/.local/state/dotman/backups')
    config.setdefault('defaults', {})
    config['defaults'].setdefault('config', {})
    config['defaults'].setdefault('colors', {})

    # Expand backup_dir
    config['backup_dir'] = os.path.expanduser(config['backup_dir'])

    return config


def load_apps() -> tuple:
    """
    Load apps.yaml and return (required_config list, apps dict).

    Returns:
        Tuple of (required_config: list, apps: dict)
    """
    data = load_yaml(DOTMAN_DIR / 'apps.yaml')

    # Extract global required_config
    required_config = data.pop('required_config', [])

    return required_config, data


def load_theme(theme_name: str, global_config: dict) -> dict:
    """
    Load a theme file and validate it has all required colors.

    Args:
        theme_name: Name of the theme (without .yaml extension)
        global_config: The global config dict from load_config()

    Returns:
        Dict with 'colors' and 'config' keys
    """
    theme_path = DOTMAN_DIR / 'themes' / f'{theme_name}.yaml'

    if not theme_path.exists():
        raise FileNotFoundError(f"Theme not found: {theme_path}")

    theme_data = load_yaml(theme_path)

    # Validate colors
    colors = theme_data.get('colors', {})
    missing = REQUIRED_COLORS - set(colors.keys())
    if missing:
        raise ValueError(
            f"Theme '{theme_name}' missing required colors: {', '.join(missing)}"
        )

    # Merge config: theme config overrides global defaults
    theme_config = global_config['defaults'].get('config', {}).copy()
    theme_config.update(theme_data.get('config', {}))

    return {
        'colors': colors,
        'config': theme_config
    }


def validate_theme(theme_name: str) -> tuple:
    """
    Validate a theme file without loading global config.

    Returns:
        Tuple of (is_valid: bool, errors: list)
    """
    theme_path = DOTMAN_DIR / 'themes' / f'{theme_name}.yaml'

    if not theme_path.exists():
        return False, [f"Theme file not found: {theme_path}"]

    try:
        data = load_yaml(theme_path)
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML syntax: {e}"]

    colors = data.get('colors', {})
    missing = REQUIRED_COLORS - set(colors.keys())

    if missing:
        return False, [f"Missing colors: {', '.join(missing)}"]

    return True, []


def list_themes() -> list:
    """Return a list of available theme names."""
    themes_dir = DOTMAN_DIR / 'themes'
    if not themes_dir.exists():
        return []

    return sorted([
        f.stem for f in themes_dir.glob('*.yaml')
    ])
