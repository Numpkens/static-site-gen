import re
from textnode import TextNode, TextType
from block_type import BlockType
from htmlnode import ParentNode, LeafNode, text_node_to_html_node

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    # NEW LINE ADDED: Handle italics using the underscore delimiter
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: missing closing '{delimiter}' delimiter")
        
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        matches = extract_markdown_images(remaining_text)
        if not matches:
            new_nodes.append(old_node)
            continue

        for alt_text, url in matches:
            parts = remaining_text.split(f"![{alt_text}]({url})", 1)
            before_image_text = parts[0]
            if before_image_text:
                new_nodes.append(TextNode(before_image_text, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = parts[1]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        matches = extract_markdown_links(remaining_text)
        if not matches:
            new_nodes.append(old_node)
            continue

        for link_text, url in matches:
            parts = remaining_text.split(f"[{link_text}]({url})", 1)
            before_link_text = parts[0]
            if before_link_text:
                new_nodes.append(TextNode(before_link_text, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            remaining_text = parts[1]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def markdown_to_blocks(markdown):
    blocks = re.split(r"(?:\n{2,})+", markdown.strip())
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block):
    lines = block.split('\n')
    if re.match(r"^#{1,6}\s", lines[0]):
        return BlockType.HEADING
    
    if len(lines) > 1 and all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(('* ', '- ')) for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(r"^\d+\.\s", line) for line in lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def block_to_paragraph(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def block_to_heading(block):
    match = re.match(r"^(#{1,6})\s(.*)", block, re.DOTALL)
    if not match:
        raise ValueError("Invalid heading block")
    level = len(match.group(1))
    text = match.group(2).strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def block_to_code(block):
    text = block[3:-3].strip()
    children = text_to_children(text)
    return ParentNode("pre", [ParentNode("code", children)])

def block_to_quote(block):
    lines = block.split('\n')
    text = "\n".join(line.lstrip('> ').strip() for line in lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)
    
def block_to_ul(block):
    items = block.split('\n')
    children = []
    for item in items:
        # CORRECTED: Use explicit stripping to avoid removing part of markdown
        if item.startswith("* "):
            text = item[2:]
        elif item.startswith("- "):
            text = item[2:]
        else:
            text = item 
        
        children.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", children)

def block_to_ol(block):
    items = block.split('\n')
    children = []
    for item in items:
        # Logic to strip the number and dot (e.g., "1. ")
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
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Markdown document must have a single h1 heading")
