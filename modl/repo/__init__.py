import shutil
from pathlib import Path

import typer

REPO_DIR = Path.home() / ".modl" / "repo"


def save_to_repo(name: str, version: str, source_path: Path):
    """Copy a model package from the local registry to the local repo."""
    dest = REPO_DIR / name / version

    if dest.exists():
        typer.echo(f"Error: {name}:{version} already exists in repo.")
        raise typer.Exit(code=1)

    dest.mkdir(parents=True)
    shutil.copytree(str(source_path), str(dest), dirs_exist_ok=True)

    typer.echo(f"Pushed {name}:{version} to local repo.")


def get_from_repo(name: str, version: str | None = None) -> tuple[Path, str]:
    """Find a model in the repo and return (path, version).

    If version is None, picks the latest version.
    """
    model_dir = REPO_DIR / name

    if not model_dir.exists():
        typer.echo(f"Error: model '{name}' not found in repo.")
        raise typer.Exit(code=1)

    if version:
        version_dir = model_dir / version
        if not version_dir.exists():
            typer.echo(f"Error: version '{version}' not found for model '{name}' in repo.")
            raise typer.Exit(code=1)
        return version_dir, version

    versions = sorted(v for v in model_dir.iterdir() if v.is_dir())
    if not versions:
        typer.echo(f"Error: no versions found for model '{name}' in repo.")
        raise typer.Exit(code=1)

    latest = versions[-1]
    return latest, latest.name
