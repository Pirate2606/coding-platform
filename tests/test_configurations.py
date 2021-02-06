import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import unittest
from app import app
from config import Config, SendMail


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config.from_object(Config)
        app.config.from_object(SendMail)
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.assertFalse(app.config["DEBUG"])

    def test_google_oauth_id(self):
        self.assertFalse("YOUR_CLIENT_ID", app.config["GOOGLE_OAUTH_CLIENT_ID"])

    def test_google_oauth_secret(self):
        self.assertFalse("YOUR_CLIENT_SECRET", app.config["GOOGLE_OAUTH_CLIENT_SECRET"])

    def test_default_config(self):
        self.assertEqual("smtp.gmail.com", app.config["MAIL_SERVER"])
        self.assertEqual(587, app.config["MAIL_PORT"])
        self.assertTrue(app.config["MAIL_USE_TLS"])
        self.assertFalse(app.config["MAIL_USE_SSL"])

    def test_mail_username(self):
        self.assertFalse('YOUR_EMAIL', app.config["MAIL_USERNAME"])

    def test_mail_password(self):
        self.assertFalse('GENERATE_PASSWORD_FOR_APP', app.config["MAIL_USERNAME"])

if __name__ == "__main__":
    unittest.main()
