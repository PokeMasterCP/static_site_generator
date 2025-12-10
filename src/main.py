#!/usr/bin/env python3
from unittest import case

from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError(f'Unsupported text type: {text_node.text_type}')

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', "", {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise ValueError(f'Unsupported text type: {text_node.text_type}')

def main():
    pass

if __name__ == '__main__':
    main()