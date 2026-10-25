import re
import shutil
import os
from dotenv import load_dotenv
from textnode import TextNode, TextType
from blockmd import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as f:
        markdown = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    html = markdown_to_html_node(markdown)
    html = html.to_html()

    title = extract_title(markdown)

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)

    with open(dest_path, 'w') as f:
        f.write(template)

    

def extract_title(markdown:str) -> str:
    title = re.findall(r'#\s(.*)', markdown)
    if title is None:
        raise Exception('Title of Page not Found')
    return title[0]

def copy_static():
    assert os.getcwd().endswith('static-site'), 'You are not running script from the root of project. DO IT!'
    if not os.path.isdir('public/'):
        print('\'public/\' directory is created')
    else:
        shutil.rmtree('public/')
        print('Everything inside public/ is deleted')

    os.mkdir('public/')

    src_path = os.path.join(os.getcwd(), 'static/')
    des_path = os.path.join(os.getcwd(), 'public/')

    file_copy(src_path, des_path)

def file_copy(file_path, des_path)-> None:
    new_file_path, new_des_path = file_path, des_path
    if os.path.isdir(file_path):
        files = os.listdir(file_path)
        for file in files:
            new_file_path = os.path.join(file_path, file)
            new_des_path = os.path.join(des_path, file)
            if not os.path.exists(new_des_path) and os.path.isdir(new_file_path):
                os.makedirs(new_des_path, exist_ok=True)
            file_copy(new_file_path, new_des_path)

    shutil.copy2(new_file_path, new_des_path)
    print(f'file: {file_path}\nis copied to {des_path}\n')
    

def main():
    copy_static()
    generate_page('content/index.md', 'template.html', 'public/index.html')
    

main()