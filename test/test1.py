import unittest
import shlex

class TestParser(unittest.TestCase):
    def test_common_args(self):
        self.assertEqual(shlex.split("ls a b"), ["ls", "a", "b"])

    def test_quoted_arg(self):
        self.assertEqual(
            shlex.split('ls "my folder" file.txt'),
            ["ls", "my folder", "file.txt"],
        )

    def test_single_quotes(self):
        self.assertEqual(
            shlex.split("cd 'home user'"),
            ["cd", "home user"],
        )

    def test_empty_input(self):
        self.assertEqual(shlex.split(""), [])

    def test_invalid_quotes(self):
        with self.assertRaises(ValueError):
            shlex.split('ls "unclosed')

class TestCommandDispatch(unittest.TestCase):
    def setUp(self):
        self.commands = {"ls", "cd", "help", "exit"}

    def test_existing_command(self):
        self.assertIn("ls", self.commands)

    def test_not_existing_command(self):
        self.assertNotIn("foo", self.commands)

if __name__ == '__main__':
    unittest.main()

