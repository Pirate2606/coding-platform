import subprocess
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

    def test_java(self):
        response = subprocess.getstatusoutput('java -version')
        self.assertEqual(0, response[0])

    def test_gcc(self):
        response = subprocess.getstatusoutput('gcc --version')
        self.assertEqual(0, response[0])

    def test_python(self):
        response = subprocess.getstatusoutput('python --version')
        self.assertEqual(0, response[0])

if __name__ == "__main__":
    unittest.main()
