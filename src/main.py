import os, shutil
from markdown_to_html import markdown_to_html_node

def copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"removed folder {destination}") 
    os.mkdir(destination)
    print(f"created folder {destination}")
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"copied file {source_path}")
        else:
            os.mkdir(destination_path)
            print(f"created folder {destination_path}")
            copy_directory(source_path, destination_path)

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("No title in document")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages(src_dir, dst_dir, template_path):
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)

        if os.path.isdir(src_path):
            # Recurse
            generate_pages(src_path, dst_path, template_path)

        elif os.path.isfile(src_path) and item == "index.md":
            os.makedirs(dst_dir, exist_ok=True)
            dst_file = os.path.join(dst_dir, "index.html")
            generate_page(src_path, template_path, dst_file)


def main():

    # root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # static -> public
    source = os.path.join(project_root, "static")
    destination = os.path.join(project_root, "public")
    copy_directory(source, destination)

    # template
    template = os.path.join(project_root, "template.html")

    # content
    content = os.path.join(project_root, "content")
    output = os.path.join(project_root, "public")

    generate_pages(content, output, template)

main()
