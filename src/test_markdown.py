import unittest

from markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_no_text_type(self):
        node = TextNode('Bold Text', TextType.BOLD)
        split_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(split_nodes[0].text_type, TextType.BOLD)

    def test_split_bold_text(self):
        node = TextNode('This text is **bold**', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(split_nodes[0], TextNode('This text is ', TextType.TEXT))
        self.assertEqual(split_nodes[1], TextNode('bold', TextType.BOLD))

    def test_split_italic_text(self):
        node = TextNode('This text is _italic_', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertEqual(split_nodes[0], TextNode('This text is ', TextType.TEXT))
        self.assertEqual(split_nodes[1], TextNode('italic', TextType.ITALIC))

    def test_split_code_text(self):
        node = TextNode('This text is `code`', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(split_nodes[0], TextNode('This text is ', TextType.TEXT))
        self.assertEqual(split_nodes[1], TextNode('code', TextType.CODE))

    def test_unclosed_markdown(self):
        node = TextNode('This is a **bold text', TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(str(context.exception), 'Invalid markdown detected.')
