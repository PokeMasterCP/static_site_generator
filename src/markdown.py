import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception('Invalid markdown detected.')

        for index in range(len(split_text)):
            if index %2 == 0:
                new_node = TextNode(split_text[index], TextType.TEXT)
                split_nodes.append(new_node)
            else:
                new_node = TextNode(split_text[index], text_type)
                split_nodes.append(new_node)

    return split_nodes

def split_nodes_image(old_nodes):
    split_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            split_nodes.append(node)
            continue
        remaining_text = node.text

        for match in matches:
            alt_text, url = match[0], match[1]
            split_list = remaining_text.split(f'![{alt_text}]({url})', 1)
            text_node = TextNode(split_list[0], TextType.TEXT)
            image_node = TextNode(alt_text, TextType.IMAGE, url)
            remaining_text = split_list[1]
            split_nodes.append(text_node)
            split_nodes.append(image_node)
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return split_nodes

def split_nodes_link(old_nodes):
    split_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            split_nodes.append(node)
            continue
        remaining_text = node.text

        for match in matches:
            alt_text, url = match[0], match[1]
            split_list = remaining_text.split(f'[{alt_text}]({url})', 1)
            text_node = TextNode(split_list[0], TextType.TEXT)
            image_node = TextNode(alt_text, TextType.LINK, url)
            remaining_text = split_list[1]
            split_nodes.append(text_node)
            split_nodes.append(image_node)
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return split_nodes

def extract_markdown_images(text):
    matches = re.findall(r'!\[(.*?)]\((.*?)\)', text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r'\[(.*?)]\((.*?)\)', text)
    return matches

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes