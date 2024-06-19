# Contributing

[![CI](https://github.com/qBraid/qBraid-CLI/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/qBraid/qBraid-CLI/actions/workflows/main.yml)
[![Documentation Status](https://readthedocs.com/projects/qbraid-qbraid-cli/badge/?version=latest)](https://docs.qbraid.com/projects/cli/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/qBraid/qBraid-CLI/graph/badge.svg?token=wVNrLILy9c)](https://codecov.io/gh/qBraid/qBraid-CLI)


Welcome! We're delighted that you're interested in contributing. Your help is essential for keeping the project great.

## Getting Started

Before you start working on a new feature or a fix, here's how you can contribute:

1. **Fork the repository**: Visit the GitHub page of our project and use the "Fork" button to create a copy of the project in your own GitHub account.
2. **Create a Development Branch**: After forking, clone the repository to your local machine and create a new branch for your development. Use a descriptive name for your branch, such as `feature-<feature-name>` or `bugfix-<bug-description>`.
3. **Commit Your Changes**: Make your changes in your development branch and commit them. Be sure to write clear, concise commit messages.
4. **Push to Your Fork**: Push your changes to your forked repository on GitHub.
5. **Create a Pull Request**: Go to the original project repository and click on "Pull Requests", then click the "New Pull Request" button

### Development install

You can install the qBraid-CLI from source by cloning this repository and running a pip install command in the root directory:

```bash
git clone https://github.com/qBraid/qBraid-CLI.git
cd qBraid-CLI
pip install -e .
```

*Note*: The current CLI configuration assumes a Linux-based filesystem. However, our goal is to move towards a platform agnostic version soon.

You can verify that the setup has been successful by checking the qBraid-CLI version with the following command:

```bash
qbraid --version
```

To view available `make` commands, run:

```bash
make help
```

## Testing

Install test dependencies:

```bash
pip install pytest
```

And run tests:

```bash
pytest tests
```

You can also run tests with make:

```bash
make test
```

## Build docs

To generate the API reference documentation locally, install the necessary requirements:

```bash
pip install -r docs/requirements.txt
```

And then run

```bash
make docs
```

Alternatively, you can generate command tree `.rst` files step-by-step:

```bash
mkdir docs/tree
typer qbraid_cli.main utils docs --name=qbraid --output=docs/tree/qbraid.md
m2r docs/tree/qbraid.md
rm docs/tree/qbraid.md
python tools/split_rst.py docs/tree/qbraid.rst
```

And then, build the docs:

```bash
sphinx-build -W -b html docs docs/build/html
```

You can view the generated documentation in your browser (on OS X) using:

```bash
open docs/build/html/index.html
```

## Code style

For code style, our project uses [ruff](https://github.com/astral-sh/ruff). Specific configurations for these tools should be added to [`pyproject.toml`](pyproject.toml).

Install linters:

```bash
pip install ruff qbraid-cli
```

Run the following and make changes as needed to satisfy format checks:

```bash
ruff format qbraid_cli tests tools
qbraid admin headers qbraid_cli tests tools --type=default --fix
```
