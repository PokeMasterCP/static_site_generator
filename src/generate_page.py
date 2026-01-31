import os

from convert_markdown import markdown_to_html_node

def extract_title(markdown):
    markdown_stripped = markdown.strip()
    if markdown_stripped[0:2] != "# ":
        raise ValueError(f'Markdown must start with an H1 heading')
    title = markdown_stripped.split("\n")[0]
    return title.strip("# ")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_content = '<article>' + markdown_to_html_node(markdown).to_html() + '</article>'
    title = '<title>' + extract_title(markdown) + '</title>'

    html = template.replace('<title>{{ Title }}</title>', title)
    html = html.replace('<article>{{ Content }}</article>', html_content)
    html = html.replace('href="./', f'href="{basepath}')
    final_html = html.replace('src="./', f'href="{basepath}')

    path = os.path.dirname(dest_path)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursively(dir_path_content, template_path, dest_path, basepath):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    
    content = os.listdir(dir_path_content)

    for file in content:
        src_file = f'{dir_path_content}/{file}'
        dest_file = f'{dest_path}/{file.replace("md", "html")}'
        if os.path.isfile(src_file):
            print(f"Using {src_file} to create {dest_file}")
            generate_page(src_file, template_path, dest_file, basepath)
            continue
        print(f'Moving into {src_file} and {dest_file}')
        generate_pages_recursively(src_file, template_path, dest_file, basepath)