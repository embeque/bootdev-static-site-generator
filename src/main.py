import re
import sys
import shutil
import os
from dotenv import load_dotenv
from textnode import TextNode, TextType
from blockmd import markdown_to_html_node

def generate_all(from_dir, dest_dir, basepath):
    assert os.getcwd().endswith('static-site'), 'You are not running script from the root of project. DO IT!'

    for item in os.listdir(from_dir):
        src_file = os.path.join(from_dir, item)
        if os.path.isfile(src_file) and src_file.endswith('.md'):
            print(f'Generating Page for file on {from_dir+'/'+item} to {dest_dir+'/'+item}')
            generate_page(os.path.join(from_dir, item), 'template.html', os.path.join(dest_dir, item), basepath)
        else: # is a dir
            generate_all(os.path.join(from_dir, item), os.path.join(dest_dir, item), basepath)

def create_missing_dirs(path):
    os.makedirs(path, exist_ok=True)

def remove_filename_from_path(path):
    if os.path.isdir(path):
        return path
    # remove the last part (works only on linux)
    path_list = path.split('/')
    path_list.pop()
    return '/'.join(path_list)

def change_format(path, format):
    path_list = path.split('/')
    last = path_list.pop()
    filename = last.split('.')[0]
    path_list.append(filename +'.'+ format)
    return '/'.join(path_list)

def generate_page(from_path, template_path, dest_path, basepath:str):
    assert os.path.exists(from_path), f"from_path: {from_path} doesn't exists. create it or change it!!"
    assert os.path.exists(template_path), f"template_path: {template_path} doesn't exists. create it or change it!!"
    
    with open(from_path, 'r') as f:
        markdown = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html_text = html_node.to_html()
    
    title = extract_title(markdown)

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html_text)
    template = template.replace('href="/', f'href="{basepath}{"/" if not basepath.endswith("/") else ""}')
    template = template.replace('src="/', f'src="{basepath}{"/" if not basepath.endswith("/") else ""}')

    dest_dir_path = remove_filename_from_path(dest_path)
    create_missing_dirs(dest_dir_path)
    # format = template_path.split('.')[1]
    format = 'html'
    dest_path = change_format(dest_path, format)

    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    with open(dest_path, 'w') as f:
        f.write(template)        


def extract_title(markdown:str) -> str:
    title = re.findall(r'#\s(.*)', markdown)
    if title is None:
        raise Exception('Title of Page not Found')
    return title[0]

def copy_static(dest_path):
    assert os.getcwd().endswith('static-site'), 'You are not running script from the root of project. DO IT!'
    if not os.path.isdir(dest_path):
        print(f'\'{dest_path}\' directory is created')
    else:
        shutil.rmtree(dest_path)
        print(f'Everything inside {dest_path} is deleted')

    os.mkdir(dest_path)

    src_path = os.path.join(os.getcwd(), 'static/')
    des_path = os.path.join(os.getcwd(), dest_path)

    file_copy(src_path, des_path)

def file_copy(file_path, des_path)-> None:
    if os.path.isfile(des_path):
        raise Exception('destination path cannot be a file, must be a folder!')

    if os.path.isfile(file_path):
        # os.makedirs(des_path, exist_ok=True)
        create_missing_dirs(des_path)
        shutil.copy2(file_path, des_path)
        print(f'file: {file_path}\nis copied to {des_path}\n')
        return

    files = os.listdir(file_path)
    for file in files:
        new_file_path, new_des_path = file_path, des_path
        # because after the loop paths are not reverted to the original
        new_file_path = os.path.join(file_path, file)
        if os.path.isdir(new_file_path):
            new_des_path = os.path.join(des_path, file)

        file_copy(new_file_path, new_des_path)

def main():
    basepath:str = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    copy_static('docs/')
    # generate_page('content/index.md', 'template.html', 'docs/index.html', basepath)
    os.makedirs('docs', exist_ok=True)
    generate_all('content', 'docs', basepath)
    

main()

