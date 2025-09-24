import re
from textnode import TextNode, TextType

# This function extract markdown image alt text and URLs from a string and returns a list of tuples, where each tuple contains (alt_text, url)
def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches

# This function exracts markdown link anchor text and urls from a string and returns a list of tuples, where each tuple contains (alt_text, url)
def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        for alt_text, url in images:
            sections = remaining_text.split(f"![{alt_text}]({url})", 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for anchor_text, url in links:
            sections = remaining_text.split(f"[{anchor_text}]({url})", 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes
