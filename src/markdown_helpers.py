import re
from textnode import TextNode, TextType
from block_type import BlockType
from htmlnode import ParentNode, LeafNode, text_node_to_html_node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Use a regex to find all matches of the delimiter
        # This is more robust than a simple split
        # The regex pattern captures the text between delimiters
        pattern = re.escape(delimiter) + r"(.*?)" + re.escape(delimiter)
        parts = re.split(f"({pattern})", node.text)

        # Check for invalid syntax
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: missing closing '{delimiter}' delimiter")

        # Process the parts
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Text outside of delimiters
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:  # Text inside of delimiters
                # Check for empty content inside the delimiters
                if part:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    # Handle empty markdown like **
                    new_nodes.append(TextNode(part, TextType.TEXT))

    return new_nodes    

def extract_markdown_images(text):
    regex = r"!\\[(.*?)\\]\\((.*?)\\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r"(?<!\\!)\\[(.*?)\\]\\((.*?)\\)"
    matches = re.findall(regex, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for alt_text, url in images:
            parts = text.split(f"![{alt_text}]({url})", 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown syntax for image")
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = parts[1]
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        for link_text, url in links:
            parts = text.split(f"[{link_text}]({url})", 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown syntax for link")
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            text = parts[1]
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(node) for node in nodes]
    return children

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block.strip() != "":
            filtered_blocks.append(block.strip())
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
        if is_quote:
            return BlockType.QUOTE
    elif block.startswith("* ") or block.startswith("- "):
        is_ul = True
        for line in lines:
            if not (line.startswith("* ") or line.startswith("- ")):
                is_ul = False
        if is_ul:
            return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        is_ol = True
        for i, line in enumerate(lines, 1):
            if not line.startswith(f"{i}. "):
                is_ol = False
        if is_ol:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_to_paragraph(block):
    return ParentNode("p", text_to_children(block))

def block_to_heading(block):
    level = block.count("#")
    text = block.lstrip("# ").strip()
    return ParentNode(f"h{level}", text_to_children(text))

def block_to_code(block):
    text = block.strip("`")
    return ParentNode("pre", [ParentNode("code", text_to_children(text))])

def block_to_quote(block):
    lines = block.split("\n")
    text = " ".join([line.lstrip('>') for line in lines])
    return ParentNode("blockquote", text_to_children(text))

def block_to_ul(block):
    items = block.split('\n')
    children = []
    for item in items:
        text = item.lstrip('-* ')
        children.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", children)

def block_to_ol(block):
    items = block.split('\n')
    children = []
    for item in items:
        text = item.split('.', 1)[1].lstrip()
        children.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", children)
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(block_to_paragraph(block))
        elif block_type == BlockType.HEADING:
            children.append(block_to_heading(block))
        elif block_type == BlockType.CODE:
            children.append(block_to_code(block))
        elif block_type == BlockType.QUOTE:
            children.append(block_to_quote(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(block_to_ul(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(block_to_ol(block))
        else:
            raise Exception("Invalid block type")
    return ParentNode("div", children)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            return stripped_line.lstrip("# ")
    raise Exception("No h1 header found")
