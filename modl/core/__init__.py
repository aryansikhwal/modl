import shutil
from pathlib import Path

import typer

from modl.archive import export_package, import_package
from modl.package import init_package, load_package
from modl.registry import save_package, get_package, get_source, list_packages, remove_package, set_tag
from modl.repo import save_to_repo, get_from_repo
from modl.runtime import run_package


def _parse_name(name: str) -> tuple[str, str | None]:
    if ":" in name:
        parts = name.split(":", 1)
        return parts[0], parts[1]
    return name, None


def init_model(name: str):
    init_package(name)


def build_model(path: str):
    config = load_package(path)
    source = {"type": "local", "path": str(Path(path).resolve())}
    save_package(config["name"], str(config["version"]), path, source)


def run_model(name: str, overrides: dict | None = None):
    model_name, version = _parse_name(name)
    path = get_package(model_name, version)
    config = load_package(str(path))
    run_package(path, config, overrides)


def serve_model(name: str, overrides: dict | None = None):
    model_name, version = _parse_name(name)
    path = get_package(model_name, version)
    config = load_package(str(path))
    port = (overrides or {}).get("port") or config.get("port", 8000)
    typer.echo(f"Serving model '{config['name']}' on port {port}...")
    run_package(path, config, overrides)


def list_models():
    models = list_packages()
    if not models:
        typer.echo("No models installed.")
        return
    typer.echo("Installed models:\n")
    for name, version in models:
        typer.echo(f"  - {name} (v{version})")


def info_model(name: str):
    model_name, version = _parse_name(name)
    path = get_package(model_name, version)
    config = load_package(str(path))

    source = get_source(model_name, version or str(config["version"]))

    typer.echo(f"Name:         {config['name']}")
    typer.echo(f"Version:      {config['version']}")
    if source:
        typer.echo(f"Source:       {source['type']} ({source['path']})")
    typer.echo(f"Entry:        {config['entry']}")
    if config.get("requirements"):
        typer.echo(f"Requirements: {config['requirements']}")
    if config.get("type"):
        typer.echo(f"Type:         {config['type']}")
    if config.get("port"):
        typer.echo(f"Port:         {config['port']}")
    if config.get("description"):
        typer.echo(f"Description:  {config['description']}")


def export_model(name: str):
    model_name, version = _parse_name(name)
    path = get_package(model_name, version)
    config = load_package(str(path))
    export_package(path, config["name"], str(config["version"]))


def import_model(file: str):
    temp_dir = import_package(file)
    try:
        config = load_package(temp_dir)
        source = {"type": "file", "path": str(Path(file).resolve())}
        save_package(config["name"], str(config["version"]), temp_dir, source)
    finally:
        shutil.rmtree(temp_dir)


def tag_model(name: str, tag: str):
    model_name, version = _parse_name(name)
    if not version:
        typer.echo("Error: version required. Use name:version format.")
        raise typer.Exit(code=1)
    set_tag(model_name, version, tag)


def push_model(name: str):
    model_name, version = _parse_name(name)
    path = get_package(model_name, version)
    config = load_package(str(path))
    save_to_repo(config["name"], str(config["version"]), path)


def pull_model(name: str):
    model_name, version = _parse_name(name)
    repo_path, resolved_version = get_from_repo(model_name, version)
    config = load_package(str(repo_path))
    source = {"type": "repo", "path": str(repo_path)}
    save_package(config["name"], resolved_version, str(repo_path), source)
    typer.echo(f"Pulled {model_name}:{resolved_version} from repo.")


def install_model(input: str):
    if input.startswith("http://") or input.startswith("https://"):
        import urllib.request
        import tempfile
        tmp = tempfile.mktemp(suffix=".mdl")
        try:
            urllib.request.urlretrieve(input, tmp)
        except Exception:
            typer.echo("[modl ERROR] Failed to download model.")
            raise typer.Exit(code=1)
        try:
            typer.echo("[modl] Installing model...")
            import_model(tmp)
            typer.echo("[modl] Installed successfully.")
        finally:
            Path(tmp).unlink(missing_ok=True)
    else:
        typer.echo("[modl] Installing model...")
        import_model(input)
        typer.echo("[modl] Installed successfully.")


def remove_model(name: str):
    remove_package(name)
