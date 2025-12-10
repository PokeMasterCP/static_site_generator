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