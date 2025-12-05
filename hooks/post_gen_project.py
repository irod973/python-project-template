import shutil
import os

def is_false(val):
    return str(val).strip().lower() in ("false", "n", "no", "0")

# Remove FastAPI component if not included
if is_false('{{cookiecutter.include_fastapi}}'):
    shutil.rmtree('src/fastapi_app', ignore_errors=True)

# Remove Metaflow component if not included
if is_false('{{cookiecutter.include_metaflow}}'):
    shutil.rmtree('src/metaflow_app', ignore_errors=True)

# Remove Python package component if not included
if is_false('{{cookiecutter.include_package}}'):
    shutil.rmtree("src/{{cookiecutter.package}}", ignore_errors=True)
    # Remove publish workflow if present
    workflow_path = os.path.join('.github', 'workflows', 'publish.yml')
    if os.path.exists(workflow_path):
        os.remove(workflow_path)
    # Remove publish badge from README if present
    readme_path = os.path.join('{{cookiecutter.repository}}', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            lines = f.readlines()
        with open(readme_path, 'w') as f:
            for line in lines:
                if 'publish.yml' not in line:
                    f.write(line)
