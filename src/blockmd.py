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

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    root_childs: list[ParentNode] = []

    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.CODE:
            text = re.findall(r'```\n([\s\S]*?)```', block)
            text_node = TextNode(text[0], TextType.CODE)
            leaf_node = text_node_to_html_node(text_node)
            parent_node = get_parent_node(BlockType.CODE, [leaf_node])
            root_childs.append(parent_node)

        else:
            block = block.replace('\n', ' ')
            children = text_to_children(block.strip())
            parent = get_parent_node(type, children)
            root_childs.append(parent)

    return ParentNode('div', root_childs)


def get_parent_node(type: BlockType, children) -> ParentNode:
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
            count = 0
            for char in children[0].value[:6]:
                if char == '#':
                    count += 1
                else: 
                    break
            return ParentNode(f'h{count}', children)
        case BlockType.QUOTE:
            return ParentNode('blockquote', children)
        


def text_to_children(block: str) -> list[LeafNode]:
    result = []
    tnodes = text_to_textnodes(block)
    for node in tnodes:
        html_node = text_node_to_html_node(node)
        result.append(html_node)

    # print(result)
    return result





#     match type:
#         case BlockType.CODE:
#             text = re.findall(r'```\n([\s\S]*?)```', block)
#             html_node = ParentNode('pre', text_t0)
#             return html

#         case BlockType.PARAGRAPH:
#             html = '<p>'
#             block = block.replace('\n', ' ')

#             nodes = text_to_textnodes(block.strip())
#             for node in nodes:
#                 leaf_node = text_node_to_html_node(node)
#                 html += leaf_node.to_html()

#             return html + '</p>'


            

def block_to_block_type(block: str) -> BlockType:
    if block[:2] == '# ':
        return BlockType.HEADING
    elif block[:4] == '```\n':
        return BlockType.CODE
    elif block[0] == '>':
        return BlockType.QUOTE
    elif block[:2] == '- ':
        return BlockType.UNORDERED_LIST
    elif block[0] in (0,1,2,3,4,5,6,7,8,9) and block[1:3] == '. ':
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> list[str]:
    md_blocks = [block.strip() for block in markdown.split('\n')]
    first, last = md_blocks[0], md_blocks[-1]
    if first == '':
        md_blocks.pop(0)
    if last == '':
        md_blocks.pop()
    md_blocks = '\n'.join(md_blocks)
    md_blocks = md_blocks.split('\n\n')
    for _ in range(md_blocks.count('')):
        md_blocks.remove('')
    
    return md_blocks


if __name__ == "__main__":
    md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
    print(text_to_children(md))

