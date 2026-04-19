import os
import subprocess
import sys
from pathlib import Path

import typer

VENVS_DIR = Path.home() / ".modl" / "venvs"


def _get_venv_python(venv_path: Path) -> str:
    if os.name == "nt":
        return str(venv_path / "Scripts" / "python.exe")
    return str(venv_path / "bin" / "python")


def _ensure_venv(config: dict) -> Path:
    venv_path = VENVS_DIR / config["name"] / str(config["version"])

    if venv_path.exists():
        return venv_path

    typer.echo("[modl] Creating virtual environment...")
    result = subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
    if result.returncode != 0:
        typer.echo("[modl ERROR] Failed to create virtual environment.")
        raise typer.Exit(code=1)

    return venv_path


def _install_requirements(path: Path, config: dict, venv_path: Path):
    marker = venv_path / ".installed"
    if marker.exists():
        typer.echo("[modl] Dependencies already installed, skipping.")
        return

    req_file = path / config.get("requirements", "requirements.txt")
    if req_file.exists() and req_file.read_text().strip() != "":
        python = _get_venv_python(venv_path)
        typer.echo("[modl] Installing dependencies...")
        result = subprocess.run(
            [python, "-m", "pip", "install", "-r", str(req_file), "--quiet"],
            cwd=str(path),
        )
        if result.returncode != 0:
            typer.echo("[modl ERROR] Failed to install requirements.")
            raise typer.Exit(code=1)

    marker.touch()


def run_package(path: Path, config: dict, overrides: dict | None = None):
    overrides = overrides or {}

    entry_file = path / config["entry"]
    if not entry_file.exists():
        typer.echo(f"[modl ERROR] Entry file '{config['entry']}' not found in {path}.")
        raise typer.Exit(code=1)

    typer.echo(f"[modl] Running model '{config['name']}' v{config['version']}")

    venv_path = _ensure_venv(config)
    typer.echo(f"[modl] Venv: {venv_path}")

    _install_requirements(path, config, venv_path)

    python = _get_venv_python(venv_path)

    cmd = [python, str(entry_file)]
    args = overrides.get("args") or config.get("args") or []
    if args:
        cmd.extend(args)

    env = os.environ.copy()
    config_env = config.get("env") or {}
    if config_env:
        env.update({str(k): str(v) for k, v in config_env.items()})
    override_env = overrides.get("env") or {}
    if override_env:
        env.update({str(k): str(v) for k, v in override_env.items()})

    port = overrides.get("port")
    if port is not None:
        env["PORT"] = str(port)

    typer.echo("[modl] Starting execution...")
    result = subprocess.run(cmd, cwd=str(path), env=env)

    if result.returncode != 0:
        typer.echo(f"[modl ERROR] Model exited with code {result.returncode}.")
        raise typer.Exit(code=result.returncode)
