import unittest

from markdown import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
                      split_nodes_image, split_nodes_link, text_to_text_nodes)
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and another ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image1", "https://i.imgur.com/zjjcJKZ.png"),
            ("image2", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)

    def test_extract_images_no_match(self):
        matches = extract_markdown_images('This is text with no images')
        self.assertListEqual([], matches)

    def test_extract_only_image(self):
        matches = extract_markdown_images("![JRR Tolkien sitting](./images/tolkien.png)")
        self.assertListEqual(
            matches,
            [("JRR Tolkien sitting", "./images/tolkien.png")]
        )

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links_no_match(self):
        matches = extract_markdown_links('This is text with no links')
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            'This is text with a link [to boot dev](https://www.boot.dev)'
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            'This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)'
        )
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ('to youtube', 'https://www.youtube.com/@bootdotdev')
        ], matches)

class TestSplitNodesImages(unittest.TestCase):
    def test_split_one_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_long_alt_text(self):
        node = TextNode(
            "This is text with a ![long alt text](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("long alt text", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_one_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )

    def test_split_two_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )

    def test_split_one_link_special_chars_in_alt_text(self):
        node = TextNode(
            "This is text with a link [to boot's dev @](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot's dev @", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes_basic(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_broken_bold_markdown_syntax(self):
        text = "This is **broken markdown."
        with self.assertRaises(Exception) as context:
            text_to_text_nodes(text)
        self.assertEqual(str(context.exception), 'Invalid markdown detected.')
