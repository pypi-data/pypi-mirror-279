# Polyharmonics

<div align="center">

![PyPI](https://img.shields.io/pypi/v/polyharmonics)
[![Python Version](https://img.shields.io/pypi/pyversions/polyharmonics.svg)](https://pypi.org/project/polyharmonics/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/ComicIvans/polyharmonics/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: ruff](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/astral-sh/ruff)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/ComicIvans/polyharmonics/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/ComicIvans/polyharmonics/releases)
[![License](https://img.shields.io/github/license/ComicIvans/polyharmonics)](https://github.com/ComicIvans/polyharmonics/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)

Ortogonal Polynomials in the unit sphere.

</div>

## Quick start

Conda package manager is recommended. Create a conda environment.

```bash
conda create -n polyharmonics python==3.10
```

Activate conda environment

```bash
conda activate polyharmonics
```

Install the package

```bash
pip install polyharmonics
```

Then you can run the client using the following command:

```bash
polyharmonics --help
```

Or with `Poetry`:

```bash
poetry run polyharmonics --help
```

### Makefile usage

[`Makefile`](https://github.com/ComicIvans/polyharmonics/blob/main/Makefile) contains a lot of functions for faster development.

<details>
<summary>Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>Codestyle and type checks</summary>
<p>

Automatic formatting uses `ruff`.

```bash
make polish-codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `ruff` and `darglint` library

</p>
</details>

<details>
<summary>Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>All linters</summary>
<p>

Of course there is a command to run all linters in one:

```bash
make lint
```

the same as:

```bash
make check-codestyle && make test && make check-safety
```

</p>
</details>

<details>
<summary>Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/ComicIvans/polyharmonics/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/ComicIvans/polyharmonics/blob/main/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/ComicIvans/polyharmonics)](https://github.com/ComicIvans/polyharmonics/blob/main/LICENSE)

This project uses the `BSD-3-Clause` license. See [LICENSE](https://github.com/ComicIvans/polyharmonics/blob/main/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{polyharmonics,
  author = {Iván Salido Cobo},
  title = {Ortogonal Polynomials in the unit sphere.},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ComicIvans/polyharmonics}}
}
```

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/Undertone0809/python-package-template)

This project was generated with [`python-package-template`](https://github.com/Undertone0809/python-package-template)
