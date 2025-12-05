import shutil

# Remove FastAPI component if not included
if '{{cookiecutter.include_fastapi}}' != 'true':
    shutil.rmtree('src/example_app', ignore_errors=True)

# Remove Metaflow component if not included
if '{{cookiecutter.include_metaflow}}' != 'true':
    shutil.rmtree('src/metaflow', ignore_errors=True)

# Remove Python package component if not included
if '{{cookiecutter.include_package}}' != 'true':
    shutil.rmtree("src/{cookiecutter.package}", ignore_errors=True)

