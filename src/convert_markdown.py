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
        sanitized_text = _sanitize_text(block, block_type)

        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(sanitized_text)
            node = ParentNode('p', children)
            html_nodes.append(node)

        elif block_type == BlockType.HEADING:
            tag = _get_heading_tag(sanitized_text)
            value = sanitized_text.strip('#')
            children = text_to_children(value)
            node = ParentNode(tag, children)
            html_nodes.append(node)

        elif block_type == BlockType.CODE:
            #value = block.strip("`\n")
            node = text_node_to_html_node(TextNode(sanitized_text, TextType.CODE))
            html_nodes.append(ParentNode('pre', [node]))

        elif block_type == BlockType.QUOTE:
            value = sanitized_text.strip('>')
            children = text_to_children(value)
            node = ParentNode('blockquote', children)
            html_nodes.append(node)

        elif block_type == BlockType.UNORDERED_LIST:
            pass
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

def _sanitize_text(text, block_type):
    if block_type == BlockType.CODE:
        return re.sub(r'^[ \s`]+', '', text, flags=re.MULTILINE)
    else:
        return re.sub(r'\s+', ' ', text)