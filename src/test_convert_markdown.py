from unittest import TestCase
from convert_markdown import markdown_to_html_node

class TestConvertMarkdownToHTMLNode(TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading6(self):
        md = """
    ###### Heading 6
    This is random text, and this is **bolded** text.
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>Heading 6 This is random text, and this is <b>bolded</b> text.</h6></div>"
        )

    def test_heading1(self):
        md = """
            # Heading 1
            This is random text, and this is _italic_ text.
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1 This is random text, and this is <i>italic</i> text.</h1></div>"
        )

    def test_quoteblock_single_line(self):
        md = """
    > This is a single line quote
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a single line quote</blockquote></div>"
        )

    def test_quoteblock_double_line(self):
        md = """
    > This is a double
    line quote
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a double line quote</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
    - Unordered Item
    - Another Unordered Item
    - Yet Another Unordered Item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Unordered Item</li><li>Another Unordered Item</li><li>Yet Another Unordered Item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
    1. First Item
    2. Second Item
    3. Third Item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First Item</li><li>Second Item</li><li>Third Item</li></ol></div>"
        )

    def test_unordered_list_of_links(self):
        md = """- [Why Glorfindel is More Impressive than Legolas](./blog/glorfindel)"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li><a href="./blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li></ul></div>'
        )
    
    def test_link_with_symbols(self):
        md = """[< Back Home](/)"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><a href="/">< Back Home</a></p></div>'
        )

    def test_bolded_with_quotes(self):
        md = '**"Váya márië."**'
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><b>"Váya márië."</b></p></div>'
        )