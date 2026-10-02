# mindfulness-MINA

Historical Python 2 Flask/WeChat backend. The public source reached its final recorded version in January 2018; it is preserved for reference, with security maintenance only. It has no supported production deployment, automated application tests, or declared license.

## Credential exposure and privacy

Earlier public commits contain database and WeChat credentials and a runtime log with identifying records. Treat both credentials as compromised: rotate or revoke them with their providers and review access logs and the historical data exposure. Removing them from this current tree does **not** remove them from Git history, forks, or existing copies. This change does not rewrite history. A history rewrite and any data-disposition decision require owner approval.

Runtime logs, bytecode, local environment files, and TLS material are excluded from new commits. Do not commit real credentials or user records.

## Configuration

Supply all six environment variables before importing the application:

- `MINA_DB_HOST`: MySQL host and optional port.
- `MINA_DB_NAME`: database name.
- `MINA_DB_USER`: database user.
- `MINA_DB_PASSWORD`: a newly issued database password.
- `MINA_WECHAT_APP_ID`: the configured WeChat application ID.
- `MINA_WECHAT_APP_SECRET`: a newly issued WeChat application secret.

`consts.py` fails closed when any required value is empty or missing. Credentials are URL-encoded when constructing the database URI and WeChat request. Do not reuse the values exposed by earlier commits.

The historical application imports Flask, Flask-SQLAlchemy, gevent and an AES provider under `Crypto.Cipher`; MySQL driver/dependency versions are not pinned. Its TLS certificate/key files are absent. Importing `Main.py` calls `db.create_all()`, and running it starts a service; perform neither against a live database for validation. Python 2, dependency compatibility, database behavior, TLS and WeChat integration remain unverified. Modernization requires a separate scoped decision.

## Safe configuration checks

Run `python3 -m unittest discover -s tests -v`. These tests import only `consts.py` in isolated subprocesses with synthetic configuration; they do not import the service, connect to a database, or call WeChat. Passing them does not validate the historical application runtime.
