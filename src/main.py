import os
import shutil

from markdown_helpers import markdown_to_html_node, extract_title
from htmlnode import ParentNode


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Check if the markdown file exists
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Markdown file not found at {from_path}")
    
    # Read the markdown content
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # Read the template content
    with open(template_path, "r") as f:
        template_content = f.read()

    # Convert markdown to an HTML node and extract the title
    html_node = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)
    
    # Convert the HTML node to a string
    html_content = html_node.to_html()

    # Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Ensure the destination directory exists
    dest_dir_path = os.path.dirname(dest_path)
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Write the final HTML to the destination file
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(from_dir_path, template_path, dest_dir_path):
    print(f"Generating pages from {from_dir_path} to {dest_dir_path}...")
    for item_name in os.listdir(from_dir_path):
        from_path = os.path.join(from_dir_path, item_name)
        dest_path = os.path.join(dest_dir_path, item_name)

        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path_final = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path_final)
        
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path)


def copy_static(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file from {source_path} to {dest_path}")
        elif os.path.isdir(source_path):
            print(f"Copying directory from {source_path} to {dest_path}")
            copy_static(source_path, dest_path)

def main():
    print("Deleting public directory...")
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
