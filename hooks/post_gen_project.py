import shutil
import os

def is_false(val: str) -> bool:
    return val.strip().lower() in ("false", "n", "no", "0")

# Remove FastAPI component if not included
if is_false("{{cookiecutter.include_fastapi}}"):
    shutil.rmtree("src/fastapi_app", ignore_errors=True)

# Remove Metaflow component if not included
if is_false("{{cookiecutter.include_metaflow}}"):
    shutil.rmtree("src/metaflow_app", ignore_errors=True)

# Remove Python package component if not included
if is_false("{{cookiecutter.include_package}}"):
    shutil.rmtree("src/{{cookiecutter.package}}", ignore_errors=True)
    # Remove publish workflow if present
    workflow_path = os.path.join(".github", "workflows", "publish.yml")
    if os.path.exists(workflow_path):
        os.remove(workflow_path)

# Remove torchvision app if not included in template options
if is_false("{{ cookiecutter.include_torchvision }}"):
    shutil.rmtree("src/torchvision_app", ignore_errors=True)
