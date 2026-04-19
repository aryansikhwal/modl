from pathlib import Path

import typer
import yaml


MODEL_YAML_TEMPLATE = {
    "name": "",
    "version": "1.0",
    "entry": "run.py",
    "requirements": "requirements.txt",
    "type": "custom",
    "description": "",
    "port": 8000,
}

OPTIONAL_DEFAULTS = {
    "requirements": None,
    "port": None,
    "type": None,
    "description": None,
    "env": {},
    "args": [],
    "tags": [],
    "labels": {},
}

RUN_PY_TEMPLATE = """\
def load_model():
    \"\"\"Load the model weights or artifacts.\"\"\"
    print("Loading model...")
    model = None
    return model


def predict(input_data):
    \"\"\"Run prediction on input data.\"\"\"
    model = load_model()
    print(f"Predicting with input: {input_data}")
    result = {}
    return result


if __name__ == "__main__":
    load_model()
    print(predict("sample input"))
"""


def init_package(name: str):
    """Create a new model package folder with template files."""
    package_dir = Path(name)

    if package_dir.exists():
        typer.echo(f"Error: folder '{name}' already exists.")
        raise typer.Exit(code=1)

    package_dir.mkdir()

    # model.yaml
    config = MODEL_YAML_TEMPLATE.copy()
    config["name"] = name
    model_yaml_path = package_dir / "model.yaml"
    model_yaml_path.write_text(yaml.dump(config, sort_keys=False))

    # run.py
    run_py_path = package_dir / "run.py"
    run_py_path.write_text(RUN_PY_TEMPLATE)

    # requirements.txt
    requirements_path = package_dir / "requirements.txt"
    requirements_path.write_text("")

    typer.echo(f"Model package '{name}' created successfully.")
    typer.echo(f"  {package_dir / 'model.yaml'}")
    typer.echo(f"  {package_dir / 'run.py'}")
    typer.echo(f"  {package_dir / 'requirements.txt'}")


REQUIRED_FIELDS = ["name", "version", "entry"]


def load_package(path: str) -> dict:
    """Read and validate a model package. Returns the parsed model.yaml config."""
    package_dir = Path(path)

    model_yaml_path = package_dir / "model.yaml"
    if not model_yaml_path.exists():
        typer.echo(f"Error: model.yaml not found in '{path}'.")
        raise typer.Exit(code=1)

    with open(model_yaml_path) as f:
        config = yaml.safe_load(f)

    # Validate required fields
    for field in REQUIRED_FIELDS:
        if field not in config or not config[field]:
            typer.echo(f"Error: missing required field '{field}' in model.yaml.")
            raise typer.Exit(code=1)

    # Check entry file exists
    entry_path = package_dir / config["entry"]
    if not entry_path.exists():
        typer.echo(f"Error: entry file '{config['entry']}' not found.")
        raise typer.Exit(code=1)

    # Apply defaults for optional fields
    for field, default in OPTIONAL_DEFAULTS.items():
        if field not in config:
            config[field] = default

    return config
