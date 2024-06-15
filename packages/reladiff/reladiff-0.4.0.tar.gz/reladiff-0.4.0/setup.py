# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reladiff', 'reladiff.databases']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1,<9.0',
 'dsnparse',
 'rich',
 'runtype>=0.4.2,<0.5.0',
 'sqeleton==0.1.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'clickhouse': ['clickhouse-driver'],
 'duckdb': ['duckdb>=0.6.0,<0.7.0'],
 'mysql': ['mysql-connector-python==8.0.29'],
 'postgresql': ['psycopg2'],
 'presto': ['presto-python-client'],
 'snowflake': ['snowflake-connector-python>=2.7.2,<3.0.0', 'cryptography'],
 'trino': ['trino>=0.314.0,<0.315.0']}

entry_points = \
{'console_scripts': ['reladiff = reladiff.__main__:main']}

setup_kwargs = {
    'name': 'reladiff',
    'version': '0.4.0',
    'description': 'Command-line tool and Python library to efficiently diff rows across two different databases.',
    'long_description': '# **reladiff**\n\n## What is `reladiff`?\nreladiff is a **free, open-source tool** that enables data professionals to detect differences in values between any two tables. It\'s fast, easy to use, and reliable. Even at massive scale.\n\n## Documentation\n\n[**🗎 Documentation website**](https://reladiff.readthedocs.io/en/latest/) - our detailed documentation has everything you need to start diffing.\n\n### Databases we support\n\n- PostgreSQL >=10\n- MySQL\n- Snowflake\n- BigQuery\n- Redshift\n- Oracle\n- Presto\n- Databricks\n- Trino\n- Clickhouse\n- Vertica\n- DuckDB >=0.6\n- SQLite (coming soon)\n\nFor their corresponding connection strings, check out our [detailed table](TODO).\n\n#### Looking for a database not on the list?\nIf a database is not on the list, we\'d still love to support it. [Please open an issue](https://github.com/erezsh/reladiff/issues) to discuss it, or vote on existing requests to push them up our todo list.\n\n## Use cases\n\n### Diff Tables Between Databases\n#### Quickly identify issues when moving data between databases\n\n<p align="center">\n  <img alt="diff2" src="https://user-images.githubusercontent.com/1799931/196754998-a88c0a52-8751-443d-b052-26c03d99d9e5.png" />\n</p>\n\n### Diff Tables Within a Database\n#### Improve code reviews by identifying data problems you don\'t have tests for\n<p align="center">\n  <a href=https://www.loom.com/share/682e4b7d74e84eb4824b983311f0a3b2 target="_blank">\n    <img alt="Intro to Diff" src="https://user-images.githubusercontent.com/1799931/196576582-d3535395-12ef-40fd-bbbb-e205ccae1159.png" width="50%" height="50%" />\n  </a>\n</p>\n\n&nbsp;\n&nbsp;\n\n## Get started\n\n### Installation\n\n#### First, install `reladiff` using `pip`.\n\n```\npip install reladiff\n```\n\n#### Then, install one or more driver(s) specific to the database(s) you want to connect to.\n\n- `pip install \'reladiff[mysql]\'`\n\n- `pip install \'reladiff[postgresql]\'`\n\n- `pip install \'reladiff[snowflake]\'`\n\n- `pip install \'reladiff[presto]\'`\n\n- `pip install \'reladiff[oracle]\'`\n\n- `pip install \'reladiff[trino]\'`\n\n- `pip install \'reladiff[clickhouse]\'`\n\n- `pip install \'reladiff[vertica]\'`\n\n- For BigQuery, see: https://pypi.org/project/google-cloud-bigquery/\n\n_Some drivers have dependencies that cannot be installed using `pip` and still need to be installed manually._\n\n### Run your first diff\n\nOnce you\'ve installed `reladiff`, you can run it from the command line.\n\n```\nreladiff DB1_URI TABLE1_NAME DB2_URI TABLE2_NAME [OPTIONS]\n```\n\nBe sure to read [the docs](TODO) for detailed instructions how to build one of these commands depending on your database setup.\n\n#### Code Example: Diff Tables Between Databases\nHere\'s an example command for your copy/pasting, taken from the screenshot above when we diffed data between Snowflake and Postgres.\n\n```\nreladiff \\\n  postgresql://<username>:\'<password>\'@localhost:5432/<database> \\\n  <table> \\\n  "snowflake://<username>:<password>@<password>/<DATABASE>/<SCHEMA>?warehouse=<WAREHOUSE>&role=<ROLE>" \\\n  <TABLE> \\\n  -k activity_id \\\n  -c activity \\\n  -w "event_timestamp < \'2022-10-10\'"\n```\n\n#### Code Example: Diff Tables Within a Database\n\nHere\'s a code example from [the video](https://www.loom.com/share/682e4b7d74e84eb4824b983311f0a3b2), where we compare data between two Snowflake tables within one database.\n\n```\nreladiff \\\n  "snowflake://<username>:<password>@<password>/<DATABASE>/<SCHEMA_1>?warehouse=<WAREHOUSE>&role=<ROLE>" <TABLE_1> \\\n  <SCHEMA_2>.<TABLE_2> \\\n  -k org_id \\\n  -c created_at -c is_internal \\\n  -w "org_id != 1 and org_id < 2000" \\\n  -m test_results_%t \\\n  --materialize-all-rows \\\n  --table-write-limit 10000\n```\n\nIn both code examples, I\'ve used `<>` carrots to represent values that **should be replaced with your values** in the database connection strings. For the flags (`-k`, `-c`, etc.), I opted for "real" values (`org_id`, `is_internal`) to give you a more realistic view of what your command will look like.\n\n### We\'re here to help!\n\nWe know that in some cases, the reladiff command can become long and dense. And maybe you\'re new to the command line.\n\n* We\'re here to help [on slack](https://locallyoptimistic.slack.com/archives/C03HUNGQV0S) if you have ANY questions as you use `reladiff` in your workflow.\n* You can also post a question in [GitHub Discussions](https://github.com/erezsh/reladiff/discussions).\n\n\nTo get a Slack invite - [click here](https://locallyoptimistic.com/community/)\n\n## How to Use\n\n* [How to use from the shell (or: command-line)](TODO)\n* [How to use from Python](TODO)\n* [How to use with TOML configuration file](TODO)\n* [Usage Analytics & Data Privacy](TODO)\n\n## How to Contribute\n* Feel free to open an issue or contribute to the project by working on an existing issue.\n* Please read the [contributing guidelines](https://github.com/erezsh/reladiff/blob/master/CONTRIBUTING.md) to get started.\n\nBig thanks to everyone who contributed so far:\n\n<a href="https://github.com/erezsh/reladiff/graphs/contributors">\n  <img src="https://contributors-img.web.app/image?repo=erezsh/reladiff" />\n</a>\n\n## Technical Explanation\n\nCheck out this [technical explanation](TODO) of how reladiff works.\n\n## License\n\nThis project is licensed under the terms of the [MIT License](https://github.com/erezsh/reladiff/blob/master/LICENSE).\n',
    'author': 'Erez Shinan',
    'author_email': 'erezshin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/erezsh/reladiff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
