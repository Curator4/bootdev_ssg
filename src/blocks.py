from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    return list(filter(None, map(str.strip, markdown.split("\n\n"))))

def block_to_block_type(block):
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    if re.match(r'^`{3}', block) and re.search(r'`{3}$', block):
        return BlockType.CODE
    lines = block.splitlines()
    if all(line.startswith(">") for line in lines): 
        return BlockType.QUOTE
    if all(re.match(r'^- ', line) for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(rf'^{i+1}\. ', line) for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
