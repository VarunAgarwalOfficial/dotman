#!/usr/bin/env python3
"""Dotman - A Minimal Dotfile Manager

Dotman allows you to manage and theme your dotfiles using Jinja2 templates
and YAML configuration. It supports variants and atomic updates with backups.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path for imports when running directly
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent))

import config
import deploy


def parse_variant_overrides(args: List[str]) -> Dict[str, str]:
    """Parse --app variant flags into a dict."""
    overrides = {}
    it = iter(args)
    for arg in it:
        if arg.startswith('--'):
            try:
                val = next(it)
                if not val.startswith('--'):
                    overrides[arg[2:]] = val
            except StopIteration:
                pass
    return overrides


def cmd_apply(args, extra_args):
    """Apply a theme to applications."""
    # Load configs
    global_config = config.load_config()
    required_vars, apps = config.load_apps()

    # Load theme
    try:
        theme_data = config.load_theme(args.theme, global_config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Parse variant overrides from extra args
    overrides = parse_variant_overrides(extra_args)

    # Filter apps if --only specified
    target_apps = apps
    if args.only:
        only_list = [a.strip() for a in args.only.split(',')]
        target_apps = {k: v for k, v in apps.items() if k in only_list}

    # Validate required config
    missing_required = [
        var for var in required_vars
        if var not in theme_data['config']
    ]
    if missing_required:
        print(f"Error: Missing required config variables: {', '.join(missing_required)}")
        print("Define them in theme config or config.yaml defaults")
        sys.exit(1)

    # Deploy each app
    success_count = 0
    total_apps = len(target_apps)

    for idx, (app_name, app_config) in enumerate(target_apps.items(), 1):
        variant = overrides.get(app_name) or app_config.get('variant')

        try:
            deploy.deploy_app(app_name, app_config, theme_data,
                           global_config, variant, args.dry_run, args.quiet, args.verbose,
                           step=idx, total_steps=total_apps)
            success_count += 1
        except Exception as e:
            if not args.quiet:
                print(f"\n[{idx}/{total_apps}] {app_name}: ERROR - {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()

    if not args.quiet:
        print(f"\nFinished: {success_count}/{total_apps} apps deployed successfully")
        if args.dry_run:
            print(f"Mode: DRY-RUN (no files were changed)")

    if not args.dry_run and success_count > 0:
        deploy.send_notification(global_config, "Theme Applied",
                                f"Applied '{args.theme}' to {success_count} apps")

    if success_count == 0:
        print("Error: No apps were deployed successfully")
        sys.exit(1)


def cmd_list(args):
    """List available themes."""
    themes = config.list_themes()

    if not themes:
        if args.plain:
            print("")
        else:
            print("No themes found in themes/ directory")
        return

    if args.plain:
        for theme in themes:
            print(theme)
    else:
        print(f"Available themes ({len(themes)}):")
        for theme in themes:
            print(f" - {theme}")


def cmd_validate(args):
    """Validate theme(s)."""
    if args.theme:
        # Validate specific theme
        is_valid, errors = config.validate_theme(args.theme)

        if is_valid:
            print(f"[OK] Theme '{args.theme}' is valid")
            return 0
        else:
            print(f"[ERROR] Theme '{args.theme}' has errors:")
            for error in errors:
                print(f"  - {error}")
            return 1
    else:
        # Validate all themes
        themes = config.list_themes()
        if not themes:
            print("No themes found to validate")
            return 0

    all_valid = True
    for theme in themes:
        is_valid, errors = config.validate_theme(theme)
        if is_valid:
            print(f"  [OK] {theme}")
        else:
            all_valid = False
            print(f"  [ERROR] {theme}")
            for error in errors:
                print(f"    - {error}")

        return 0 if all_valid else 1


def create_parser():
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog='dotman',
        description='Dotman - A Minimal Dotfile Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s apply catppuccin              # Apply catppuccin theme to all apps
  %(prog)s apply gruvbox --only hyprland,waybar  # Apply to specific apps only
  %(prog)s apply catppuccin --dry-run    # Preview changes without applying
  %(prog)s apply catppuccin --hyprland dark      # Use 'dark' variant for hyprland
  %(prog)s list                          # Show available themes
  %(prog)s validate                      # Validate all themes
  %(prog)s validate catppuccin           # Validate specific theme

App-specific overrides:
  Use --<app_name> <variant> to override the variant for a specific app.
  Example: --hyprland dark --waybar minimal

Configuration files:
  config.yaml      - Global settings and defaults
  apps.yaml        - App registry with targets, templates, variants
  themes/*.yaml    - Theme definitions with colors and config

For more information, see dotman.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Apply command
    apply_parser = subparsers.add_parser(
        'apply',
        help='Apply a theme to applications',
        description='Apply a theme to configured applications.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dotman apply catppuccin
  dotman apply gruvbox --only hyprland
  dotman apply catppuccin --dry-run --only waybar
  dotman apply catppuccin --hyprland dark --waybar minimal
        """
    )
    apply_parser.add_argument(
        'theme',
        help='Theme name (from themes/ directory)'
    )
    apply_parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Preview changes without modifying files'
    )
    apply_parser.add_argument(
        '--only',
        metavar='APPS',
        help='Comma-separated list of apps to apply (e.g., hyprland,waybar)'
    )
    apply_parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress output except for errors'
    )
    apply_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed error information'
    )

    # List command
    list_parser = subparsers.add_parser(
        'list',
        help='List available themes',
        description='Show all available themes in the themes/ directory.'
    )
    list_parser.add_argument(
        '--plain', '-p',
        action='store_true',
        help='Output plain theme names only (for scripts)'
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate theme configuration',
        description='Validate theme YAML files for required colors.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dotman validate              # Validate all themes
  dotman validate catppuccin   # Validate specific theme
        """
    )
    validate_parser.add_argument(
        'theme',
        nargs='?',
        help='Theme name to validate (optional)'
    )

    return parser


def main():
    parser = create_parser()
    args, extra = parser.parse_known_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'apply':
            cmd_apply(args, extra)
        elif args.command == 'list':
            cmd_list(args)
        elif args.command == 'validate':
            sys.exit(cmd_validate(args))
    except KeyboardInterrupt:
        print("\nOperation cancelled")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
