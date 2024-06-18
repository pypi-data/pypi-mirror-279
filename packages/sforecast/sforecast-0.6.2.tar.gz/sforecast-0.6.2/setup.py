# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sforecast']

package_data = \
{'': ['*']}

install_requires = \
['beautifulplots>=0.2.6',
 'pandas>=1.4.0',
 'pmdarima>=1.8.0',
 'regex>=2024.5.15,<2025.0.0',
 'scikit-learn>=1.4.2',
 'scipy>=1.13.1,<2.0.0',
 'statsmodels>=0.13.2',
 'tensorflow>=2.7.0',
 'xgboost>=2.0.3']

setup_kwargs = {
    'name': 'sforecast',
    'version': '0.6.2',
    'description': 'A framework for running forecasting models within a sliding/expanding window out-of-sample forecast fit (train/test) and prediction (forecasts). The package includes support of classical forecasting models, SK Learn supervised learning ML models, and TensorFlow deep learning models.',
    'long_description': '# sforecast\n\nA framework for running forecasting models within a sliding (expanding) window out-of-sample fit (train/test) and prediction (forecasts). The package includes support of classical forecasting models, SK Learn ML models, and TensorFlow deep learning models.\n\n- https://sforecast.readthedocs.io/en/latest/\n\n## Installation\n\n```bash\n$ pip install sforecast\n```\n\n## License\n\n`sforecast` was created by Alberto Gutierrez. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`sforecast` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Alberto Gutierrez',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
