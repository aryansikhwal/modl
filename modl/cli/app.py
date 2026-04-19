from typing import Optional

import typer

from modl import core

VERSION = "0.1.0"

def _version_callback(value: bool):
    if value:
        typer.echo(f"modl v{VERSION}")
        raise typer.Exit()

app = typer.Typer(help="modl — package, run, and serve AI/ML models locally.")

@app.callback()
def main(
    version: Optional[bool] = typer.Option(None, "--version", callback=_version_callback, is_eager=True, help="Show version and exit"),
):
    pass


@app.command()
def init(name: str = typer.Argument(help="Name of the model package to create")):
    """Create a new model package template."""
    core.init_model(name)


@app.command()
def build(path: str = typer.Argument(help="Path to the model package folder")):
    """Validate and store a model in the local registry."""
    core.build_model(path)


@app.command()
def run(
    name: str = typer.Argument(help="Name of the model to run"),
    env: Optional[list[str]] = typer.Option(None, "--env", help="Override env var (KEY=VALUE)"),
    arg: Optional[list[str]] = typer.Option(None, "--arg", help="Override args"),
    port: Optional[int] = typer.Option(None, "--port", help="Override port"),
):
    """Run a model locally."""
    overrides = _build_overrides(env, arg, port)
    core.run_model(name, overrides)


@app.command()
def serve(
    name: str = typer.Argument(help="Name of the model to serve"),
    env: Optional[list[str]] = typer.Option(None, "--env", help="Override env var (KEY=VALUE)"),
    arg: Optional[list[str]] = typer.Option(None, "--arg", help="Override args"),
    port: Optional[int] = typer.Option(None, "--port", help="Override port"),
):
    """Serve a model as an API server."""
    overrides = _build_overrides(env, arg, port)
    core.serve_model(name, overrides)


def _build_overrides(
    env: Optional[list[str]],
    arg: Optional[list[str]],
    port: Optional[int],
) -> dict:
    overrides = {}
    if env:
        env_dict = {}
        for item in env:
            if "=" not in item:
                typer.echo(f"Error: invalid env format '{item}'. Use KEY=VALUE.")
                raise typer.Exit(code=1)
            key, value = item.split("=", 1)
            env_dict[key] = value
        overrides["env"] = env_dict
    if arg:
        overrides["args"] = arg
    if port is not None:
        overrides["port"] = port
    return overrides


@app.command(name="list")
def list_models():
    """List all installed models."""
    core.list_models()


@app.command()
def info(name: str = typer.Argument(help="Name of the model to inspect")):
    """Show details about a built model."""
    core.info_model(name)


@app.command(name="export")
def export_model(name: str = typer.Argument(help="Name of the model to export")):
    """Export a model to a .mdl archive file."""
    core.export_model(name)


@app.command(name="import")
def import_model(file: str = typer.Argument(help="Path to the .mdl file to import")):
    """Import a model from a .mdl archive file."""
    core.import_model(file)


@app.command()
def tag(
    name: str = typer.Argument(help="Model name:version to tag"),
    tag: str = typer.Argument(help="Tag name (e.g. latest)"),
):
    """Assign a tag to a model version."""
    core.tag_model(name, tag)


@app.command()
def push(name: str = typer.Argument(help="Name of the model to push")):
    """Push a model to the local repo."""
    core.push_model(name)


@app.command()
def pull(name: str = typer.Argument(help="Name of the model to pull from repo")):
    """Pull a model from the local repo into the registry."""
    core.pull_model(name)


@app.command()
def install(file: str = typer.Argument(help="Path or URL of the .mdl file to install")):
    """Install a model from a .mdl archive file or URL."""
    core.install_model(file)


@app.command()
def remove(name: str = typer.Argument(help="Name of the model to remove")):
    """Remove a model from the local registry."""
    core.remove_model(name)
