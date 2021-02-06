import unittest
from pathlib import Path
import pkg_resources


# _REQUIREMENTS_PATH = Path(__file__).with_name("requirements.txt")
_REQUIREMENTS_PATH = Path(__file__).parent.with_name("requirements.txt")

class BasicTests(unittest.TestCase):
    # Testing ROUTES

    def test_requirements(self):
        requirements = pkg_resources.parse_requirements(_REQUIREMENTS_PATH.open())
        for requirement in requirements:
            requirement = str(requirement)
            with self.subTest(requirement=requirement):
                pkg_resources.require(requirement)

if __name__ == "__main__":
    unittest.main()
