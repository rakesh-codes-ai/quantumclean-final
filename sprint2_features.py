name: Release

# Publishes the package when a version tag (e.g. v1.0.0) is pushed.
on:
  push:
    tags:
      - "v*"

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install build tooling
        run: python -m pip install --upgrade pip build twine
      - name: Run tests before releasing
        run: |
          pip install -e ".[dev,ml]"
          pytest -q
      - name: Build distribution
        run: python -m build
      - name: Check distribution
        run: twine check dist/*
      # Publishing step (uncomment and add a PyPI token secret to go live):
      # - name: Publish to PyPI
      #   env:
      #     TWINE_USERNAME: __token__
      #     TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      #   run: twine upload dist/*
