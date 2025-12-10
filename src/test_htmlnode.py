import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_normal(self):
        node = HTMLNode('<a>', 'google link', None, {'href': 'https://www.google.com'} )
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_prop_only(self):
        node = HTMLNode(None, None, None, {'href': 'https://www.google.com'})
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html_long_dict(self):
        prop = {
            'href': 'https://www.google.com',
            'key_1': 'value_1',
            'key_2': 'value_2',
            'key_3': 'value_3'
        }
        node = HTMLNode(None, None, None, prop)
        expected = ' href="https://www.google.com" key_1="value_1" key_2="value_2" key_3="value_3"'
        self.assertEqual(node.props_to_html(), expected)

class LeafNodeTest(unittest.TestCase):
    def test_leaf_to_html_a(self):
        node = LeafNode('a', 'google', {'href': 'https://www.google.com'})
        expected = '<a href="https://www.google.com">google</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode('p', 'example text')
        expected = '<p>example text</p>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None,"raw text", None)
        expected = 'raw text'
        self.assertEqual(node.to_html(), expected)

class ParentNodeTest(unittest.TestCase):
    def test_parent_to_html_mixed(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), expected)

    def test_parent_to_html_nested_parents(self) :
        parent_inner_1 = ParentNode(
            'head',
            [
                LeafNode('title', 'Sample title'),
                LeafNode('style', 'p: {color: blue}')
            ]
        )
        parent_inner_2 = ParentNode(
            'body',
            [
                LeafNode('p', "Sample text"),
                LeafNode('a', 'sample link', {'href': 'https://www.google.com'})
            ]
        )

        parent_outer = ParentNode('html', [parent_inner_1, parent_inner_2])
        expected = '<html><head><title>Sample title</title><style>p: {color: blue}</style></head><body><p>Sample text</p><a href="https://www.google.com">sample link</a></body></html>'
        self.assertEqual(parent_outer.to_html(), expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
