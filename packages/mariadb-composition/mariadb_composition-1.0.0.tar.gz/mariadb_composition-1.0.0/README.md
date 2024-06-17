# mariadb_composition

SQL String Composition for MariaDB

This module is based on [psycopg.sql](https://www.psycopg.org/psycopg3/docs/api/sql.html), but generates SQL for mariadb and does it without depending on a live connection to the db.

## Usage

Works pretty much like <https://www.psycopg.org/psycopg3/docs/api/sql.html#module-usage>

It would be good to improve this documentation.

## Contributing

1. Clone the repo.
2. Set up your venv:
    1. `python3 -m venv .venv`
    2. `source .venv/bin/activate`
3. Get the Requirements: `python3 -m pip install -r requirements.txt`
4. `hatch test` to run the tests (add `-c` to see coverage info)
5. Make changes/write tests.
6. Open a PR.
