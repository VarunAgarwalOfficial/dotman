"""Template rendering and color filters for Dotman."""

import os
from jinja2 import Environment, FileSystemLoader


def strip_hex(value: str) -> str:
    """Remove # from hex color."""
    return value.lstrip('#') if isinstance(value, str) else value


def hex_to_rgb(value: str) -> str:
    """Convert #RRGGBB to R, G, B."""
    if not isinstance(value, str) or len(value) != 7:
        return value
    value = value.lstrip('#')
    try:
        return f"{int(value[0:2], 16)}, {int(value[2:4], 16)}, {int(value[4:6], 16)}"
    except ValueError:
        return value


def hex_to_rgba(value: str, alpha: float = 0.5) -> str:
    """Convert hex to rgba(R, G, B, A)."""
    rgb = hex_to_rgb(value)
    return f"rgba({rgb}, {alpha})"


def hex_to_argb(value: str) -> str:
    """Convert #RRGGBB to 0xffRRGGBB (Hyprland format)."""
    return value.replace('#', '0xff') if isinstance(value, str) else value


FILTERS = {
    'hex': lambda x: x,  # pass-through
    'strip': strip_hex,
    'rgb': hex_to_rgb,
    'rgba': hex_to_rgba,
    'argb': hex_to_argb,
}


def apply_filters(colors: dict, filter_names: list) -> dict:
    """
    Apply filters to all colors.

    Args:
        colors: Dict of color_name -> hex_value
        filter_names: List of filter names to apply

    Returns:
        New dict with filtered colors
    """
    result = colors.copy()

    for name in filter_names:
        if name not in FILTERS or name == 'rgba':
            print(f"Warning: Filter '{name}' not supported for auto-expansion")
            continue

        func = FILTERS[name]
        for key, value in result.items():
            if isinstance(value, str):
                try:
                    result[key] = func(value)
                except Exception:
                    pass

    return result


def render_template(template_path: str, context: dict) -> str:
    """
    Render a Jinja2 template with the given context.

    Args:
        template_path: Path to the template file
        context: Dict of variables to pass to template

    Returns:
        Rendered template as string
    """
    template_dir = os.path.dirname(template_path) or '.'
    template_file = os.path.basename(template_path)

    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters.update(FILTERS)

    try:
        template = env.get_template(template_file)
        return template.render(context)
    except Exception as e:
        raise RuntimeError(f"Error rendering {template_path}: {e}")


def build_context(theme_data: dict) -> dict:
    """
    Build the template context from theme data.

    Args:
        theme_data: Dict with 'colors' and 'config' keys

    Returns:
        Context dict for template rendering
    """
    context = {}

    # Add colors dict and individual color variables
    context['colors'] = theme_data['colors'].copy()
    context.update(theme_data['colors'])

    # Add config variables (gap, border_size, etc.)
    context.update(theme_data.get('config', {}))

    return context
