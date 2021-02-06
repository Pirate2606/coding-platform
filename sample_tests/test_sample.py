import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import unittest
import datetime
from app import app, get_dateTime
from config import Config, SendMail


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.assertFalse(app.config["DEBUG"])

    def test_datetime(self):
        dateTime = ["30 Mar 2020", "00:00:00"]
        result = get_dateTime(dateTime)
        self.assertEqual(datetime.datetime(2020, 3, 30, 0, 0), result)

    def test_main_page(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
