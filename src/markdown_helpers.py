import re

# This function extract markdown image alt text and URLs from a string and returns a list of tuples, where each tuple contains (alt_text, url)
def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches

# This function exracts markdown link anchor text and urls from a string and returns a list of tuples, where each tuple contains (alt_text, url)
def extract_markdown_links(text):
    regex = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches
