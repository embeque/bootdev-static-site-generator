from textnode import TextNode, TextType

import re

def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.PLAINTEXT)
    bolds = split_nodes_delimiter([node], '**', TextType.BOLD)
    italics = split_nodes_delimiter(bolds, '_', TextType.ITALIC)
    codes = split_nodes_delimiter(italics, '`', TextType.CODE)
    links = split_nodes_link(codes)
    images = split_nodes_image(links)
    # can be any order due to negative lookbehind regex
    return images





# changing from function from   findall -> search
# changing the definition form  list[tuple[str, str]] -> re.Match
def extract_markdown_images(raw: str) -> re.Match|None:
    regex = r'\!\[(.*?)\]\((.*?)\)'
    return re.search(regex, raw)

def extract_markdown_links(raw: str) -> re.Match|None:
    regex = r'(?<!\!)\[(.*?)\]\((.*?)\)'
    return re.search(regex, raw)
    

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    if delimiter == '': # don't know why i do that
        return old_nodes
    
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAINTEXT:
            result.append(node)
            continue

        text_list = node.text.split(delimiter)
        if len(text_list) == 1:
            result.append(node) # this is a plaintext 
            # but don't contain the delimiter
            continue
        elif len(text_list) < 3:
            raise Exception('delimiter doesn\'t have a closing end')

        start = TextNode(text_list.pop(0), TextType.PLAINTEXT)
        end = TextNode(text_list.pop(), TextType.PLAINTEXT)

        inline = TextNode(delimiter.join(text_list), text_type)
        if inline.text.find(delimiter) != -1:
            inline = split_nodes_delimiter([inline], delimiter, text_type)

        result.extend([start, inline, end])

    return result

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAINTEXT:
            result.append(node)
            continue

        match = extract_markdown_images(node.text)
        end = node
        while match is not None:
            start = TextNode(match.string[ : match.start()], TextType.PLAINTEXT)
            end = TextNode(match.string[match.end():], TextType.PLAINTEXT)
            link = TextNode(match.groups()[0], TextType.IMAGE, match.groups()[1])

            result.extend([start, link])

            match = extract_markdown_images(end.text)

        if end.text != '':
            result.append(end)

    result = list(filter(lambda x: x.text != '', result))
    print('split image result', result)
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAINTEXT:
            result.append(node)
            continue

        match = extract_markdown_links(node.text)
        end = node
        while match is not None:
            start = TextNode(match.string[ : match.start()], TextType.PLAINTEXT)
            end = TextNode(match.string[match.end():], TextType.PLAINTEXT)
            link = TextNode(match.groups()[0], TextType.LINK, match.groups()[1])

            result.extend([start, link])

            match = extract_markdown_links(end.text)

        if end.text != '':
            result.append(end)

    result = list(filter(lambda x: x.text != '', result))
    print('split link result', result)
    return result



# def get_type_with_del(delimiter:str) -> TextType:
#     if delimiter == '**':
#         return TextType.BOLD
#     elif delimiter == '_':
#         return TextType.ITALIC
#     elif delimiter == '`':
#         return TextType.CODE
    
#     return TextType.PLAINTEXT


if __name__ == "__main__":
    # output = extract_markdown_images('This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)')
    # print(type(output))
    # print(output)

    output = text_to_textnodes('This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)')
    assert(output == [
        TextNode("This is ", TextType.PLAINTEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.PLAINTEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.PLAINTEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.PLAINTEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.PLAINTEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ])
