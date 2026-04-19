import tarfile
import tempfile
from pathlib import Path

import typer


def export_package(path: Path, name: str, version: str) -> Path:
    """Create a .mdl (tar.gz) archive from a package directory.

    Returns the path to the created archive file.
    """
    output_file = Path(f"{name}-{version}.mdl")

    with tarfile.open(str(output_file), "w:gz") as tar:
        for item in path.iterdir():
            tar.add(str(item), arcname=item.name)

    typer.echo(f"Exported {name}:{version} -> {output_file}")
    return output_file


def import_package(file: str) -> tuple[str, dict]:
    """Extract a .mdl archive to a temp directory.

    Returns (temp_dir_path, config) for the registry to pick up.
    """
    archive_path = Path(file)

    if not archive_path.exists():
        typer.echo(f"Error: file '{file}' not found.")
        raise typer.Exit(code=1)

    if not archive_path.name.endswith(".mdl"):
        typer.echo("Error: file must be a .mdl archive.")
        raise typer.Exit(code=1)

    temp_dir = tempfile.mkdtemp(prefix="modl_import_")

    try:
        with tarfile.open(str(archive_path), "r:gz") as tar:
            tar.extractall(temp_dir)
    except tarfile.TarError:
        typer.echo("[modl ERROR] Invalid model file.")
        typer.echo("Make sure the URL points to a direct .mdl download.")
        raise typer.Exit(code=1)

    return temp_dir
