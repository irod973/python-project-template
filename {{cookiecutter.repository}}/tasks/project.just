# run project tasks
[group('project')]
project: project-requirements

# export requirements file
[group('project')]
project-requirements:
    uv export --format=requirements-txt --no-dev --no-hashes \
        --no-editable --no-emit-project --output-file=requirements.txt
