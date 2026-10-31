from enum import Enum
import re
from splitting import text_to_textnodes
from htmlnode import *
from textnode import * 

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'ulist'
    ORDERED_LIST = 'olist'

def extract_block_text(block:str, type:BlockType)-> tuple[str, int]:
    if type == BlockType.CODE:
        regex = r'```\n([\s\S]*?)```'
        text = re.findall(regex, block)[0]
        return text, 0
    elif type == BlockType.HEADING:
        # replaced previously - maybe i should remove it
        block = block.replace('\n', ' ')
        regex = r'(#*)\s(.*)'
        headcount, text = re.findall(regex, block)[0]
        return text, len(headcount)
    elif type == BlockType.QUOTE:
        regex = r'>\s?(.*)'
        text = re.findall(regex, block)
        return '%%%'.join(text), 0
    elif type == BlockType.ORDERED_LIST:
        regex = r'\d.\s(.*)'
        text = re.findall(regex, block)
        return '%%%'.join(text), 0
    elif type == BlockType.UNORDERED_LIST:
        regex = r'-\s(.*)'
        text = re.findall(regex, block)
        return '%%%'.join(text), 0
    elif type == BlockType.PARAGRAPH:
        # don't do it in paragraphs unless necessary
        # block = block.replace('\n', ' ')
        return block, 0
    # else:



def markdown_to_html_node(markdown: str) -> ParentNode:
    # debugging
    print('Markdown text read from file:\n', markdown)

    blocks = markdown_to_blocks(markdown)
    
    # for later to define
    root_childs: list[ParentNode] = []

    
    for block in blocks:
        type = block_to_block_type(block)

        main_text, headcount = extract_block_text(block, type)

        # child of code is by default, updated as need
        children:list[LeafNode] = [text_node_to_html_leaf_node(TextNode(main_text, TextType.CODE))]
        if type != BlockType.CODE:
            children = get_children_leaf_node_from_text(main_text, type)
        parent = get_parent_node(type, children, headcount)

        # debugging
        print(f'\n\nMain_text:\n{main_text}')
        print(f'parent({type}): {parent}\nchildren:{children}')
        
        root_childs.append(parent)

    # got all root childs
    root = ParentNode('div', root_childs)
    return root














    # blocks = markdown_to_blocks(markdown)

    # root_childs: list[ParentNode] = []

    # for block in blocks:
    #     type = block_to_block_type(block)
    #     if type == BlockType.CODE:
    #         text = re.findall(r'```\n([\s\S]*?)```', block)
    #         text_node = TextNode(text[0], TextType.CODE)
    #         leaf_node = text_node_to_html_leaf_node(text_node)
    #         parent_node = get_parent_node(BlockType.CODE, [leaf_node])
    #         root_childs.append(parent_node)
        
    #     # create seperate process for headings
    #     elif type == BlockType.HEADING:
    #         block = block.replace('\n', ' ')
    #         regex = r'(#*)\s(.*)'
    #         pattern = re.findall(regex, block)
    #         headc, texte = pattern[0]
    #         children = text_to_children(texte.strip())
    #         parent = get_parent_node(type, children, len(headc))
    #         root_childs.append(parent)
    #     elif type == BlockType.QUOTE:
    #         regex = r'>\s(.*)'
    #         pattern = re.findall(regex, block)
    #         text = '\n'.join(pattern)
    #         children = text_to_children(text.strip())
    #         parent = get_parent_node(type, children)
    #         root_childs.append(parent)
    #     elif type == BlockType.ORDERED_LIST:
    #         regex = r'\d.\s(.*)'
    #         pattern = re.findall(regex, block)
    #         text = '\n'.join(pattern)
    #         children = text_to_children(text.strip())
    #         children = list(map(lambda x: ParentNode('li', [x]), children))
    #         parent = get_parent_node(type, children)
    #         root_childs.append(parent)
            
    #     elif type == BlockType.UNORDERED_LIST:
    #         regex = r'-\s(.*)'
    #         pattern = re.findall(regex, block)
    #         text = '\n'.join(pattern)
    #         children = text_to_children(text.strip())
    #         children = list(map(lambda x: ParentNode('li', [x]), children))
    #         parent = get_parent_node(type, children)
    #         root_childs.append(parent)
            

    #     else:
    #         # block = block.replace('\n', ' ')
    #         children = text_to_children(block.strip())
    #         parent = get_parent_node(type, children)
    #         root_childs.append(parent)

    # return ParentNode('div', root_childs)


def get_parent_node(type: BlockType, children, head_count:int=0) -> ParentNode:
    match type:
        case BlockType.CODE:
            return ParentNode('pre', children)
        case BlockType.PARAGRAPH:
            return ParentNode('p', children)
        case BlockType.UNORDERED_LIST:
            return ParentNode('ul', children)
        case BlockType.ORDERED_LIST:
            return ParentNode('ol', children)
        case BlockType.HEADING:
            return ParentNode(f'h{head_count}', children)
        case BlockType.QUOTE:
            return ParentNode('blockquote', children)
        

# changed from text_to_children()
def get_children_leaf_node_from_text(block: str, type) -> list[LeafNode]:
    # every type except code will come in
    # we have to return its children
    result = []
    items = block.split('%%%')

    for item in items:
        text_nodes = []
        text_nodes.extend(text_to_textnodes(item))
        children = []
        for node in text_nodes:
            leafnode = text_node_to_html_leaf_node(node)
            children.append(leafnode)
        # children will have many leaf nodes at this moment
        if type == BlockType.UNORDERED_LIST or type == BlockType.ORDERED_LIST:
            result.append(ParentNode('li', children))
        else:
            result.extend(children)
    # print(result)
    return result

            

def block_to_block_type(block: str) -> BlockType:
    if block.startswith('#'):
        return BlockType.HEADING
    elif block.startswith('```'):
        return BlockType.CODE
    elif block.startswith('>'):
        return BlockType.QUOTE
    elif block.startswith('-'):
        return BlockType.UNORDERED_LIST
    elif block.startswith('1'):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    return non-empty blocks of markdown splitted on \n
    """

    blocks =  [block.strip() for block in markdown.split('\n\n') if block.strip()]

    # for debugging
    print('\n\n blocked formed from markdown')
    for i in range(len(blocks)):
        print(f'Block {i}:\n{blocks[i]}')
    print('\n all the block ends \n')

    return blocks





    # md_blocks = [block.strip() for block in markdown.split('\n')]
    # first, last = md_blocks[0], md_blocks[-1]
    # if first == '':
    #     md_blocks.pop(0)
    # if last == '':
    #     md_blocks.pop()
    # md_blocks = '\n'.join(md_blocks)
    # md_blocks = md_blocks.split('\n\n')
    # for _ in range(md_blocks.count('')):
    #     md_blocks.remove('')
    
    # return md_blocks


if __name__ == "__main__":
    md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
    print(get_children_leaf_node_from_text(md))

