import subprocess
import unittest

class BasicTests(unittest.TestCase):
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
