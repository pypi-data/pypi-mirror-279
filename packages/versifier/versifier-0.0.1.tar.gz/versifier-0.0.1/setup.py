# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versifier']

package_data = \
{'': ['*']}

install_requires = \
['click==8.0.3',
 'pip-requirements-parser>=32.0.1,<33.0.0',
 'tomli>=1.2.3,<2.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses==0.8']}

entry_points = \
{'console_scripts': ['versifier = versifier.__main__:cli']}

setup_kwargs = {
    'name': 'versifier',
    'version': '0.0.1',
    'description': 'Versifier: A lyrical tool to transform Python requirements into Poetry configurations, effortlessly and elegantly.',
    'long_description': '# versifier\n\n[![Release](https://img.shields.io/github/v/release/mrlyc/versifier)](https://img.shields.io/github/v/release/mrlyc/versifier)\n[![Build status](https://img.shields.io/github/actions/workflow/status/mrlyc/versifier/main.yml?branch=main)](https://github.com/mrlyc/versifier/actions/workflows/main.yml?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/mrlyc/versifier/branch/main/graph/badge.svg)](https://codecov.io/gh/mrlyc/versifier)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/mrlyc/versifier)](https://img.shields.io/github/commit-activity/m/mrlyc/versifier)\n[![License](https://img.shields.io/github/license/mrlyc/versifier)](https://img.shields.io/github/license/mrlyc/versifier)\n\nVersifier: A lyrical tool to transform Python requirements into Poetry configurations, effortlessly and elegantly.\n\n- **Github repository**: <https://github.com/mrlyc/versifier/>\n- **Documentation** <https://mrlyc.github.io/versifier/>\n\n## Getting started with your project\n\nFirst, create a repository on GitHub with the same name as this project, and then run the following commands:\n\n```bash\ngit init -b main\ngit add .\ngit commit -m "init commit"\ngit remote add origin git@github.com:mrlyc/versifier.git\ngit push -u origin main\n```\n\nFinally, install the environment and the pre-commit hooks with\n\n```bash\nmake install\n```\n\nYou are now ready to start development on your project!\nThe CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.\n\nTo finalize the set-up for publishing to PyPi or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).\nFor activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).\nTo enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).\n\n## Releasing a new version\n\n- Create an API Token on [Pypi](https://pypi.org/).\n- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/mrlyc/versifier/settings/secrets/actions/new).\n- Create a [new release](https://github.com/mrlyc/versifier/releases/new) on Github.\n- Create a new tag in the form `*.*.*`.\n\nFor more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'MrLYC',
    'author_email': 'fx@m.mrlyc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrlyc/versifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
