import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_diff(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_None(self):
        node = TextNode('This is a test node', TextType.LINK, None)
        node2 = TextNode('This is a test node', TextType.LINK, 'google.com')
        self.assertNotEqual(node, node2)

    def test_diff_text(self):
        node = TextNode('Test text 1', TextType.TEXT)
        node2 = TextNode('Test text 2', TextType.TEXT)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()