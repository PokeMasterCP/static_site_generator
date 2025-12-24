import unittest

from blocknode import block_to_block_type, BlockType, markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_remove_empty_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items



        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_single_header(self):
        md = "# This is a header"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_single_line_code_block(self):
        md = "```This is a single line code block.```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_multi_line_code_block(self):
        md = """```
This is a code block
```
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_single_line_quote_block(self):
        md = ">This is a quote block"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_multi_line_quote_block(self):
        md = """> This is a quote block line 1
> This is a quote block line 2
> This is a quote block line 3
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list(self):
        md = """-Option 1
-Option 2
-Option 3
        """
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        md = """1. Item 1
2. Item 2
3. Item 3
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_out_of_order(self):
        md = """1. Item 1
3. Item 3
2. Item 2
"""
        with self.assertRaises(Exception) as context:
            block_type = block_to_block_type(md)
        self.assertEqual(str(context.exception), 'Invalid ordered list detected.')

    def test_normal_paragraph(self):
        md = "This is a normal paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)