import re

from blocknode import markdown_to_blocks, block_to_block_type, BlockType
from markdown import text_to_text_nodes, text_node_to_html_node
from textnode import TextNode, TextType
from src.htmlnode import ParentNode


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            sanitized_text = _sanitize_text(block)
            children = text_to_children(sanitized_text)
            node = ParentNode('p', children)
            html_nodes.append(node)

        elif block_type == BlockType.HEADING:
            tag = _get_heading_tag(block)
            value = block.strip('#')
            children = text_to_children(value)
            node = ParentNode(tag, children)
            html_nodes.append(node)

        elif block_type == BlockType.CODE:
            value = block.strip('`')
            node = text_node_to_html_node(TextNode(value, TextType.CODE))
            html_nodes.append(node)

        elif block_type == BlockType.QUOTE:
            value = block.strip('>')
            children = text_to_children(value)
            node = ParentNode('blockquote', children)
            html_nodes.append(node)

        elif block_type == BlockType.UNORDERED_LIST:
            value = block.strip('')

    return ParentNode('div', html_nodes)

def _get_heading_tag(block):
    i = 0
    while block[i] == '#':
        i += 1
    return f'h{i}'

def text_to_children(text):
    children = []
    text_nodes = text_to_text_nodes(text)
    for node in text_nodes:
        child = text_node_to_html_node(node)
        children.append(child)
    return children

def _sanitize_text(text):
    return re.sub(r'\s+', ' ', text)