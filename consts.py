# coding=utf-8
"""Deployment configuration; no credentials are supplied by the repository."""
import os
try:
    from urllib.parse import quote
except ImportError:  # Python 2 deployment used by this historical application
    from urllib import quote


def required_env(name):
    value = os.environ.get(name)
    if not value or not value.strip():
        raise RuntimeError("Required environment variable is missing: " + name)
    return value


HOSTNAME = required_env("MINA_DB_HOST")
DATABASE = required_env("MINA_DB_NAME")
USERNAME = required_env("MINA_DB_USER")
PASSWORD = required_env("MINA_DB_PASSWORD")
DB_URI = "mysql://{0}:{1}@{2}/{3}".format(
    quote(USERNAME, safe=""), quote(PASSWORD, safe=""), HOSTNAME,
    quote(DATABASE, safe=""))
WECHAT_APP_ID = required_env("MINA_WECHAT_APP_ID")
WECHAT_APP_SECRET = required_env("MINA_WECHAT_APP_SECRET")
