from blocks import BlockType, markdown_to_blocks, block_to_block_type
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextType, TextNode, text_node_to_html_node
from splitnodes import text_to_textnodes
import re

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                node = handle_paragraph(block)
                block_html_nodes.append(node)
            case BlockType.HEADING:
                node = handle_heading(block)
                block_html_nodes.append(node)
            case BlockType.CODE:
                node = handle_code(block)
                block_html_nodes.append(node)
            case BlockType.QUOTE:
                node = handle_quote(block)
                block_html_nodes.append(node)
            case BlockType.UNORDERED_LIST:
                node = handle_unordered_list(block)
                block_html_nodes.append(node)
            case BlockType.ORDERED_LIST:
                node = handle_ordered_list(block)
                block_html_nodes.append(node)
            case _:
                raise ValueError("unknown BlockType")
    return ParentNode(tag="div", children=block_html_nodes)

def find_heading(block):
    match = re.match(r'^(#+)', block)
    heading_size = len(match.group(1))
    if heading_size > 6 or heading_size < 1:
        raise ValueError("Could not determing heading size")
    return f"h{heading_size}"

def text_to_children(block):
    textnodes = text_to_textnodes(block)
    children = [text_node_to_html_node(node) for node in textnodes]
    return children

def handle_paragraph(block):
    text = " ".join(block.splitlines())
    children = text_to_children(text)
    return ParentNode(tag="p", children=children)

def handle_heading(block):
    tag = find_heading(block)
    text = block.lstrip("# ")
    children = text_to_children(text)
    return ParentNode(tag=tag, children=children)

def handle_code(block):
    lines = block.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    text = "\n".join(lines) + "\n"
    return ParentNode(tag="pre", children=[LeafNode(tag="code", value=text)])

def handle_quote(block):
    text = " ".join([line.lstrip("> ") for line in block.splitlines()])
    children = text_to_children(text)
    return ParentNode(tag="blockquote", children=children)

def handle_unordered_list(block):
    lines = [line.lstrip("- ") for line in block.splitlines()]
    list_items = [ParentNode(tag="li", children=text_to_children(line)) for line in lines]
    return ParentNode(tag="ul", children=list_items)

def handle_ordered_list(block):
    lines = [re.sub(r'^\d+\. ', "", line) for line in block.splitlines()]
    list_items = [ParentNode(tag="li", children=text_to_children(line)) for line in lines]
    return ParentNode(tag="ol", children=list_items)
