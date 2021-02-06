import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import datetime
import unittest
from app import get_dateTime, createFile, complier_output, app


class BasicTests(unittest.TestCase):

    def test_datetime(self):
        dateTime = ["30 Mar 2020", "00:00:00"]
        result = get_dateTime(dateTime)
        self.assertEqual(datetime.datetime(2020, 3, 30, 0, 0), result)

    def test_createFile(self):
        createFile("print('Hello')", "Python")
        self.assertTrue(os.path.exists('try.py'))

        createFile("#include <stdio.h>\nint main() {\nprintf('Hello, World!');\nreturn 0;\n}", "C")
        self.assertTrue(os.path.exists('try.c'))

        createFile("class main {\npublic static void main(String[] args) {\nSystem.out.println('Hello, World!');\n}\n}", "Java")
        self.assertTrue(os.path.exists('try.java'))

    def test_compiler_output(self):
        result = complier_output("print('Hello')", "", "", "Python")
        self.assertEqual('Hello', result.strip())

    def test_compiler_output_with_input(self):
        result = complier_output("x = input()\nprint(x)", "testing", "", "Python")
        self.assertEqual('testing', result.strip())


if __name__ == "__main__":
    unittest.main()
