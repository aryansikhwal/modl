import json
import shutil
from pathlib import Path

import typer

REGISTRY_DIR = Path.home() / ".modl" / "models"


def save_package(name: str, version: str, source_path: str, source: dict | None = None):
    """Copy a model package into the local registry."""
    dest = REGISTRY_DIR / name / str(version)

    if dest.exists():
        typer.echo(f"Error: model {name}:{version} already exists.")
        raise typer.Exit(code=1)

    dest.mkdir(parents=True)
    shutil.copytree(source_path, str(dest), dirs_exist_ok=True)

    # Write source tracking metadata
    if source:
        source_file = dest / "source.json"
        with open(source_file, "w") as f:
            json.dump(source, f, indent=2)

    typer.echo(f"Built {name}:{version}")


def get_source(name: str, version: str) -> dict | None:
    """Read source.json for a model version. Returns None if not found."""
    resolved = _resolve_version(name, version) if version else None
    if resolved:
        source_file = REGISTRY_DIR / name / resolved / "source.json"
    else:
        path = get_package(name)
        source_file = path / "source.json"
    if not source_file.exists():
        return None
    with open(source_file) as f:
        return json.load(f)


def get_package(name: str, version: str | None = None) -> Path:
    """Find a model in the registry and return its path.

    If version is given, use it. Otherwise pick the latest version.
    """
    model_dir = REGISTRY_DIR / name

    if not model_dir.exists():
        typer.echo(f"Error: model '{name}' not found in registry.")
        raise typer.Exit(code=1)

    if version:
        resolved = _resolve_version(name, version)
        version_dir = model_dir / resolved
        if not version_dir.exists():
            typer.echo(f"Error: version '{version}' not found for model '{name}'.")
            raise typer.Exit(code=1)
        return version_dir

    versions = sorted(v for v in model_dir.iterdir() if v.is_dir())
    if not versions:
        typer.echo(f"Error: no versions found for model '{name}'.")
        raise typer.Exit(code=1)

    return versions[-1]


def list_packages() -> list[tuple[str, str]]:
    """List all models in the registry. Returns list of (name, version) tuples."""
    if not REGISTRY_DIR.exists():
        return []

    results = []
    for model_dir in sorted(REGISTRY_DIR.iterdir()):
        if not model_dir.is_dir():
            continue
        for version_dir in sorted(model_dir.iterdir()):
            if version_dir.is_dir():
                results.append((model_dir.name, version_dir.name))

    return results


def _load_tags(name: str) -> dict:
    """Load tags.json for a model. Returns empty dict if not found."""
    tags_file = REGISTRY_DIR / name / "tags.json"
    if not tags_file.exists():
        return {}
    with open(tags_file) as f:
        return json.load(f)


def _save_tags(name: str, tags: dict):
    """Save tags.json for a model."""
    tags_file = REGISTRY_DIR / name / "tags.json"
    with open(tags_file, "w") as f:
        json.dump(tags, f, indent=2)


def set_tag(name: str, version: str, tag: str):
    """Assign a tag to a specific version of a model."""
    model_dir = REGISTRY_DIR / name

    if not model_dir.exists():
        typer.echo(f"Error: model '{name}' not found in registry.")
        raise typer.Exit(code=1)

    version_dir = model_dir / version
    if not version_dir.exists():
        typer.echo(f"Error: version '{version}' not found for model '{name}'.")
        raise typer.Exit(code=1)

    tags = _load_tags(name)
    tags[tag] = version
    _save_tags(name, tags)

    typer.echo(f"Tagged {name}:{version} as '{tag}'.")


def _resolve_version(name: str, version_or_tag: str) -> str:
    """If version_or_tag matches a tag, return the real version. Otherwise return as-is."""
    tags = _load_tags(name)
    return tags.get(version_or_tag, version_or_tag)


def remove_package(name: str):
    """Delete a model and all its versions from the registry."""
    model_dir = REGISTRY_DIR / name

    if not model_dir.exists():
        typer.echo(f"Error: model '{name}' not found in registry.")
        raise typer.Exit(code=1)

    shutil.rmtree(model_dir)
    typer.echo(f"Model '{name}' removed from registry.")
