"""Backup and deployment for Dotman."""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from template import render_template, build_context
from config import DOTMAN_DIR


def backup_target(target_dir: str, backup_dir: str, app_name: str, specific_files: list | None = None):
    """
    Backup existing target directory.

    Args:
        target_dir: Path to the target directory
        backup_dir: Directory to store backup
        app_name: Name of the app (used for subfolder)
        specific_files: If provided, only backup these files (relative paths)
    """
    target_path = Path(target_dir).expanduser()
    backup_path = Path(backup_dir) / datetime.now().strftime("%Y-%m-%d_%H-%M-%S") / app_name

    if not target_path.exists():
        return

    backup_path.mkdir(parents=True, exist_ok=True)

    if specific_files:
        # Only backup specific files
        for filename in specific_files:
            src = target_path / filename
            if src.exists() and not src.is_symlink():
                dst = backup_path / filename
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_file():
                    shutil.copy2(src, dst)
                elif src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        # Backup entire directory (skip symlinks)
        for item in target_path.rglob('*'):
            if item.is_symlink():
                continue
            if item.is_file():
                rel_path = item.relative_to(target_path)
                dst = backup_path / rel_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst)


def get_source_files(template_dir: str, variant: str | None = None, specific_files: list | None = None) -> dict:
    """
    Get mapping of source files to render.

    Args:
        template_dir: Base template directory (relative to DOTMAN_DIR)
        variant: Optional variant name
        specific_files: If provided, only include these files

    Returns:
        Dict mapping relative_path -> full_source_path
    """
    files = {}
    base_template_dir = DOTMAN_DIR / template_dir
    base_dir = base_template_dir / 'base'
    variant_dir = base_template_dir / variant if variant else None

    # Start with base files
    if base_dir.exists():
        for src in base_dir.rglob('*'):
            if src.is_file():
                rel = src.relative_to(base_dir)
                files[str(rel)] = str(src)

    # Overlay variant files (overwrites base)
    if variant_dir and variant_dir.exists():
        for src in variant_dir.rglob('*'):
            if src.is_file():
                rel = src.relative_to(variant_dir)
                files[str(rel)] = str(src)

    # If specific files requested, filter to only those
    if specific_files:
        filtered = {}
        for spec in specific_files:
            # Find any file matching this spec
            for rel_path, full_path in files.items():
                if Path(rel_path).name == spec or rel_path == spec:
                    # Use filename as destination (not full path)
                    filtered[spec] = full_path
                    break
            else:
                print(f"Warning: File '{spec}' not found in template")
        return filtered

    return files


def deploy_app(app_name: str, app_config: dict, theme_data: dict,
               config: dict, variant: str | None = None, dry_run: bool = False,
               quiet: bool = False, verbose: bool = False, step: int = 1, total_steps: int = 1):
    """Deploy a single application with step tracking."""
    target = os.path.expanduser(app_config['target'])
    template = app_config['template']
    specific_files = app_config.get('files', None)
    reload_cmd = app_config.get('reload')
    should_backup = app_config.get('backup', True)

    errors = []
    files_deployed = 0
    files_count = 0

    if not quiet:
        status = "DRY-RUN" if dry_run else "DEPLOY"
        var_str = f"({variant})" if variant else "(base)"
        print(f"\n[{step}/{total_steps}] {app_name} {var_str} [{status}]")
        print(f"  target: {target}")

    # Get source files
    try:
        file_map = get_source_files(template, variant, specific_files)
        files_count = len(file_map)
        if not quiet:
            print(f"  files: {files_count}")
    except Exception as e:
        raise RuntimeError(f"resolving files: {e}")

    if not file_map:
        raise RuntimeError(f"no files found in template")

    # Backup
    if not dry_run and should_backup:
        try:
            backup_target(target, config['backup_dir'], app_name, specific_files)
            if not quiet:
                print(f" backup: created")
        except Exception as e:
            if not quiet:
                print(f" backup: failed - {e}")
    elif not dry_run and not should_backup:
        if not quiet:
            print(f" backup: skipped (disabled for this app)")

    # Build template context
    context = build_context(theme_data)

    # Deploy files
    for dest_name, src_path in file_map.items():
        dest_path = os.path.join(target, dest_name)

        if dry_run:
            if not quiet:
                print(f"    {src_path} -> {dest_path}")
            continue

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        try:
            # Remove symlinks before writing (they may point to root-owned files)
            if os.path.islink(dest_path):
                os.remove(dest_path)

            content = render_template(src_path, context)
            with open(dest_path, 'w') as f:
                f.write(content)
            files_deployed += 1

            if os.access(src_path, os.X_OK):
                os.chmod(dest_path, os.stat(dest_path).st_mode | 0o111)

            if verbose and not quiet:
                print(f"    {dest_name} -> written")

        except Exception as e:
            errors.append(f"{src_path}: {e}")
            if not quiet:
                print(f"    {dest_name} -> ERROR: {e}")

    # Reload (fire-and-forget for commands that don't exit, like waybar)
    if reload_cmd and not dry_run:
        try:
            subprocess.Popen(reload_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not quiet:
                print(f"  reload: triggered")
        except Exception as e:
            if not quiet:
                print(f"  reload: failed ({e})")

    if not quiet:
        if errors:
            print(f"  result: {files_deployed}/{files_count} files, {len(errors)} errors")
        else:
            print(f"  result: {files_deployed}/{files_count} files, done")

    if errors:
        raise RuntimeError(f"{len(errors)} file(s) failed to deploy")


def send_notification(config: dict, title: str, message: str):
    """Send system notification if enabled."""
    try:
        subprocess.run(['notify-send', '-a', 'Dotman', title, message],
                      check=False, capture_output=True)
    except FileNotFoundError:
        pass  # notify-send not installed
