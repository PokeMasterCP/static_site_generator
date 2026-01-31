from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    block_strings = []
    split_strings = markdown.split('\n\n')
    for string in split_strings:
        string = string.strip()
        if string:
            block_strings.append(string)
    return block_strings

def block_to_block_type(block):
    if re.match(r'^#{1,6}', block):
        return BlockType.HEADING
    elif re.match(r'^`{3}[\s\S]+?`{3}$', block) or re.match(r'^`[\s\S]+?`$', block):
        return BlockType.CODE
    elif re.match(r'(m?)^>.+', block):
        return BlockType.QUOTE
    elif re.match(r'(m?)^-.+', block):
        return BlockType.UNORDERED_LIST
    elif re.match(r'(?m)^\s*\d+\.\s+', block):
        index = 1
        for line in block.split('\n'):
            counter = line.strip()
            if counter and int(counter[0]) != index:
                raise Exception('Invalid ordered list detected.')
            index += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

