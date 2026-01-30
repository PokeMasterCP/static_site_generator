import os

from convert_markdown import markdown_to_html_node

def extract_title(markdown):
    markdown_stripped = markdown.strip()
    if markdown_stripped[0:2] != "# ":
        raise ValueError(f'Markdown must start with an H1 heading')
    title = markdown_stripped.split("\n")[0]
    return title.strip("# ")

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_content = '<article>' + markdown_to_html_node(markdown).to_html() + '</article>'
    title = '<title>' + extract_title(markdown) + '</title>'

    html_with_title = template.replace('<title>{{ Title }}</title>', title)
    final_html = html_with_title.replace('<article>{{ Content }}</article>', html_content)

    path = os.path.dirname(dest_path)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(dest_path, 'w') as f:
        f.write(final_html)
