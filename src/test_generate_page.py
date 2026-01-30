from unittest import TestCase

from generate_page import extract_title

class TestExtractTitle(TestCase):
    def test_valid_input(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, 'Hello')

    def test_invalid_input_h2(self):
        md = "## Hello"
        with self.assertRaises(ValueError) as context:
            title = extract_title(md)
        self.assertEqual(str(context.exception), 'Markdown must start with an H1 heading')

    def test_valid_input_with_newline(self):
        md = "# Hello\nWorld"
        title = extract_title(md)
        self.assertEqual(title, 'Hello')