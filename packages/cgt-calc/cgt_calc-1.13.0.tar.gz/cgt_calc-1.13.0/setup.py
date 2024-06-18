# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgt_calc', 'cgt_calc.parsers', 'cgt_calc.resources']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<4.0.0',
 'pandas>=2.0.3,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'types-requests>=2.27.7,<3.0.0',
 'yfinance>=0.2.36,<0.3.0']

entry_points = \
{'console_scripts': ['cgt-calc = cgt_calc.main:init']}

setup_kwargs = {
    'name': 'cgt-calc',
    'version': '1.13.0',
    'description': 'UK capital gains tax calculator for Charles Schwab and Trading 212 accounts',
    'long_description': '[![CI](https://github.com/KapJI/capital-gains-calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/KapJI/capital-gains-calculator/actions)\n[![PyPI version](https://img.shields.io/pypi/v/cgt-calc)](https://pypi.org/project/cgt-calc/)\n\n# UK capital gains calculator\n\nCalculate capital gains tax by transaction history exported from Charles Schwab, Trading 212 and Morgan Stanley. Generate PDF report with calculations.\n\nAutomatically convert all prices to GBP and apply HMRC rules to calculate capital gains tax: "same day" rule, "bed and breakfast" rule, section 104 holding.\n\n## Report example\n\n[calculations_example.pdf](https://github.com/KapJI/capital-gains-calculator/blob/main/calculations_example.pdf)\n\n## Installation\n\nInstall it with [pipx](https://pypa.github.io/pipx/) (or regular pip):\n\n```shell\npipx install cgt-calc\n```\n\n## Prerequisites\n\n-   Python 3.8 or above.\n-   `pdflatex` is required to generate the report.\n-   [Optional] Docker\n\n## Install LaTeX\n\n### MacOS\n\n```shell\nbrew install --cask mactex-no-gui\n```\n\n### Debian based\n\n```shell\napt install texlive-latex-base\n```\n\n### Windows\n\n[Install MiKTeX.](https://miktex.org/download)\n\n### Docker\n\nThese steps will build and run the calculator in a self-contained environment, in case you would rather not have a systemwide LaTeX installation (or don\'t want to interfere with an existing one).\nThe following steps are tested on an Apple silicon Mac and may need to be slightly modified on other platforms.\nWith the cloned repository as the current working directory:\n\n```shell\n$ docker buildx build --platform linux/amd64 --tag capital-gains-calculator .\n```\n\nNow you\'ve built and tagged the calculator image, you can drop into a shell with `cgt-calc` installed on `$PATH`. Navigate to where you store your transaction data, and run:\n\n```shell\n$ cd ~/Taxes/Transactions\n$ docker run --rm -it -v "$PWD":/data capital-gains-calculator:latest\na4800eca1914:/data# cgt-calc [...]\n```\n\nThis will create a temporary Docker container with the current directory on the host (where your transaction data is) mounted inside the container at `/data`. Follow the usage instructions below as normal,\nand when you\'re done, simply exit the shell. You will be dropped back into the shell on your host, with your output report pdf etc..\n\n## Usage\n\nYou will need several input files:\n\n-   Exported transaction history from Schwab in CSV format since the beginning.\n    Or at least since you first acquired the shares, which you were holding during the tax year. Schwab only allows to download transaction for the last 4 years so keep it safe. After that you may need to restore transactions from PDF statements.\n    [See example](https://github.com/KapJI/capital-gains-calculator/blob/main/tests/test_data/schwab_transactions.csv).\n-   Exported transaction history from Schwab Equity Awards (e.g. for Alphabet/Google employees) since the beginning (Note: Schwab now allows for the whole history of Equity Awards account transactions to be downloaded). These are to be downloaded in JSON format. Instructions are available at the top of the [parser file](../main/cgt_calc/parsers/schwab_equity_award_json.py).\n-   Exported transaction history from Trading 212.\n    You can use several files here since Trading 212 limit the statements to 1 year periods.\n    [See example](https://github.com/KapJI/capital-gains-calculator/tree/main/tests/test_data/trading212).\n-   Exported transaction history from Morgan Stanley.\n    Since Morgan Stanley generates multiple files in a single report, please specify a directory produced from the report download page.\n-   Exported transaction history from Sharesight\n    Sharesight is a portfolio tracking tool with support for multiple brokers.\n\n    You will need the "All Trades" and "Taxable Income" reports since the beginning.\n    Make sure to select "Since Inception" for the period, and "Not Grouping".\n    Export both reports to Excel or Google Sheets, save as CSV, and place them in the same folder.\n\n    Sharesight aggregates transactions from multiple brokers, but doesn\'t necessarily have balance information.\n    Use the `--no-balance-check` flag to avoid spurious errors.\n\n    Since there is no direct support for equity grants, add `Stock Activity` as part of the comment associated with any vesting transactions - making sure they have the grant price filled.\n\n    [See example](https://github.com/KapJI/capital-gains-calculator/tree/main/tests/test_data/sharesight).\n\n-   CSV file with initial stock prices in USD at the moment of vesting, split, etc.\n    [`initial_prices.csv`](https://github.com/KapJI/capital-gains-calculator/blob/main/cgt_calc/resources/initial_prices.csv) comes pre-packaged, you need to use the same format.\n-   (Optional) Monthly exchange rates prices from [gov.uk](https://www.gov.uk/government/collections/exchange-rates-for-customs-and-vat).\n    `exchange_rates.csv` gets generated automatically using HMRC API, you need to use the same format if you want to override it.\n\nThen run (you can omit the brokers you don\'t use):\n\n```shell\ncgt-calc --year 2020 --schwab schwab_transactions.csv --trading212 trading212/ --mssb mmsb_report/\n```\n\nSee `cgt-calc --help` for the full list of settings.\n\n## Disclaimer\n\nPlease be aware that I\'m not a tax adviser so use this data at your own risk.\n\n## Contribute\n\nAll contributions are highly welcomed.\nIf you notice any bugs please open an issue or send a PR to fix it.\n\nFeel free to add new parsers to support transaction history from more brokers.\n\n## Testing\n\nThis project uses [Poetry](https://python-poetry.org/) for managing dependencies.\n\n-   For local testing you need to [install it](https://python-poetry.org/docs/#installation).\n-   After that run `poetry install` to install all dependencies.\n-   Then activate `pre-commit` hook: `poetry run pre-commit install`\n\nYou can also run all linters and tests manually with this command:\n\n```shell\npoetry run pre-commit run --all-files\n```\n',
    'author': 'Ruslan Sayfutdinov',
    'author_email': 'ruslan@sayfutdinov.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/KapJI/capital-gains-calculator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
