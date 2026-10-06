"""Configuration-only checks; never import Main.py or connect to services."""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = {
    "MINA_DB_HOST": "localhost:3306", "MINA_DB_NAME": "test_db",
    "MINA_DB_USER": "test/user", "MINA_DB_PASSWORD": "synthetic@password:/",
    "MINA_WECHAT_APP_ID": "synthetic-app", "MINA_WECHAT_APP_SECRET": "synthetic-secret",
}


class ConfigurationTests(unittest.TestCase):
    def run_config(self, values, code="import consts"):
        env = dict(os.environ)
        for key in CONFIG:
            env.pop(key, None)
        env.update(values)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        process = subprocess.Popen([sys.executable, "-c", code], cwd=ROOT,
                                   env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode, stdout.decode("utf-8"), stderr.decode("utf-8")

    def test_each_setting_required_without_secret_in_error(self):
        for key in CONFIG:
            values = dict(CONFIG)
            values.pop(key)
            status, stdout, stderr = self.run_config(values)
            self.assertNotEqual(status, 0)
            self.assertIn("Required environment variable is missing: " + key, stderr)
            for value in CONFIG.values():
                self.assertNotIn(value, stdout + stderr)

    def test_blank_setting_rejected(self):
        values = dict(CONFIG)
        values["MINA_DB_PASSWORD"] = "  "
        status, _, stderr = self.run_config(values)
        self.assertNotEqual(status, 0)
        self.assertIn("MINA_DB_PASSWORD", stderr)

    def test_valid_settings_encode_database_credentials(self):
        code = ("import consts; "
                "assert consts.DB_URI == 'mysql://test%2Fuser:synthetic%40password%3A%2F@localhost:3306/test_db'; "
                "assert consts.WECHAT_APP_ID == 'synthetic-app'; "
                "assert consts.WECHAT_APP_SECRET == 'synthetic-secret'")
        status, stdout, stderr = self.run_config(CONFIG, code)
        self.assertEqual(status, 0, stderr)
        self.assertEqual(stdout, "")


if __name__ == "__main__":
    unittest.main()
