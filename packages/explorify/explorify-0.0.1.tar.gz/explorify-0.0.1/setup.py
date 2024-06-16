# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['explorify',
 'explorify.eda',
 'explorify.eda.bivariate',
 'explorify.eda.data_prep',
 'explorify.eda.multivariate',
 'explorify.eda.regression',
 'explorify.eda.stats',
 'explorify.eda.stats.descriptive',
 'explorify.eda.stats.distribution',
 'explorify.eda.stats.inferential',
 'explorify.eda.univariate',
 'explorify.eda.visualize',
 'explorify.utils']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs-material',
 'mkdocstrings[python]>=0.23',
 'mypy',
 'pre-commit',
 'pymdown-extensions',
 'pytest',
 'pytest-cov',
 'pytest-github-actions-annotate-failures',
 'python-kacl',
 'ruff>=0.2.0']

setup_kwargs = {
    'name': 'explorify',
    'version': '0.0.1',
    'description': 'Explorify: Your modular solution for comprehensive data exploration. Dive deep with a suite of statistical techniques, tests, and visualizations designed for flexibility and ease of use.',
    'long_description': "# Explorify\n\n[![PyPI](https://img.shields.io/pypi/v/explorify?style=flat-square)](https://pypi.python.org/pypi/explorify/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/explorify?style=flat-square)](https://pypi.python.org/pypi/explorify/)\n[![PyPI - License](https://img.shields.io/pypi/l/explorify?style=flat-square)](https://pypi.python.org/pypi/explorify/)\n[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)\n\n---\n\n**Documentation**: [https://variancexplained.github.io/explorify](https://variancexplained.github.io/explorify)\n\n**Source Code**: [https://github.com/variancexplained/explorify](https://github.com/variancexplained/explorify)\n\n**PyPI**: [https://pypi.org/project/explorify/](https://pypi.org/project/explorify/)\n\n---\n\nExplorify: Your modular solution for comprehensive data exploration. Dive deep with a suite of statistical techniques, tests, and visualizations designed for flexibility and ease of use.\n\n## Installation\n\n```sh\npip install explorify\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.8+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](https://github.com/variancexplained/explorify/tree/master/docs) and from the docstrings\n of the public signatures of the source code. The documentation is updated and published as a [Github Pages page](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/variancexplained/explorify/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/variancexplained/explorify/releases) and publish it. When\n a release is published, it'll trigger [release](https://github.com/variancexplained/explorify/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatting (`ruff format`), linters (e.g. `ruff` and `mypy`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n",
    'author': 'John James',
    'author_email': 'john@variancexplained.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://variancexplained.github.io/explorify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
