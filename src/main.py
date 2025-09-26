import os
import shutil
import sys  # Added for CLI argument handling

from markdown_helpers import markdown_to_html_node, extract_title
from htmlnode import ParentNode


def copy_static(source_dir, dest_dir):
    """
    Recursively copies contents from source_dir to dest_dir.
    """
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    if os.path.exists(dest_dir):
        # Delete and recreate the destination directory
        print(f"Deleting {dest_dir} directory...")
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
            # Recursive call to handle subdirectories
            copy_static(source_path, dest_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read files (omitted file existence checks for brevity but they should be in place)
    with open(from_path, "r") as f:
        markdown_content = f.read()

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
    
    # Replace hardcoded root paths with the dynamic basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Ensure the destination directory exists
    dest_dir_path = os.path.dirname(dest_path)
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Write the final HTML to the destination file
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(from_dir_path, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for item_name in os.listdir(from_dir_path):
        from_path = os.path.join(from_dir_path, item_name)
        dest_path = os.path.join(dest_dir_path, item_name)

        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path_final = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path_final, basepath)
        
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def main():
    # Get basepath from CLI argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # Use 'docs' instead of 'public' for GitHub Pages
    copy_static("static", "docs") # <-- This line is now correctly linked to the function above
    print("Generating pages from content to docs...")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
