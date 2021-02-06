import unittest
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from app import app


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.assertFalse(app.config["DEBUG"])

    def test_main_page(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_compile_page(self):
        tester = app.test_client(self)
        response = tester.get('/compile')
        self.assertEqual(response.status_code, 200)

    def test_contest_page(self):
        tester = app.test_client(self)
        response = tester.get('/contest', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_practice_page(self):
        tester = app.test_client(self)
        response = tester.get('/practice', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_profile_page(self):
        tester = app.test_client(self)
        response = tester.get('/profile', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_submit_page(self):
        tester = app.test_client(self)
        response = tester.post('/submit', data={'code':'print("Hello")', 'input':'', 'check':'0', 'comp_select':'Python'})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
