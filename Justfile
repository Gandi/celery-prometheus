package := 'celery_prometheus'

install:
    uv sync

lint:
    uv run ruff check .

typecheck:
    uv run mypy src/

fmt:
    uv run ruff check --fix .
    uv run ruff format src

release major_minor_patch: changelog
    #! /bin/bash
    # Try to bump the version first
    if ! uvx pdm bump {{major_minor_patch}}; then
        # If it fails, check if pdm-bump is installed
        if ! uvx pdm self list | grep -q pdm-bump; then
            # If not installed, add pdm-bump
            uvx pdm self add pdm-bump
        fi
        # Attempt to bump the version again
        uvx pdm bump {{major_minor_patch}}
    fi
    uv sync

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(uv run scripts/get_version.py)"
    git push
    git tag "v$(uv run scripts/get_version.py)"
    git push origin "v$(uv run scripts/get_version.py)"
