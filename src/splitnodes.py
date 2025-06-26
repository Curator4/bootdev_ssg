from textnode import TextType, TextNode
import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(sep=delimiter)
            for index, text in enumerate(split_text):
                if index % 2 == 0:
                    if text != "":
                        new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            remaining_text = node.text
            for image_alt, image_link in images:
                parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                if len(parts) != 2:
                    raise ValueError("invalid markdown, link section not closed")
                text, remaining_text = parts
                if text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            remaining_text = node.text
            for anchor_text, url in links:
                parts = remaining_text.split(f"[{anchor_text}]({url})", 1)
                if len(parts) != 2:
                    raise ValueError("invalid markdown, link section not closed")
                text, remaining_text = parts
                if text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
