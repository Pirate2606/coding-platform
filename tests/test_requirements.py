import unittest
from pathlib import Path
import pkg_resources
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import app


_REQUIREMENTS_PATH = Path(__file__).parent.with_name("requirements.txt")

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.assertFalse(app.config["DEBUG"])

    def test_requirements(self):
        requirements = pkg_resources.parse_requirements(_REQUIREMENTS_PATH.open())
        for requirement in requirements:
            requirement = str(requirement)
            with self.subTest(requirement=requirement):
                pkg_resources.require(requirement)

if __name__ == "__main__":
    unittest.main()
