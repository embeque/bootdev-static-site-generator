from enum import Enum
from htmlnode import LeafNode, ParentNode

class TextType(Enum):
    PLAINTEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text: str, text_type: TextType, url = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node: 'TextNode') -> bool:
        istext = self.text == text_node.text
        istext_type = self.text_type == text_node.text_type
        is_url = self.url == text_node.url

        if istext and istext_type and is_url:
            return True
        return False

    def __repr__(self) -> str:
        return f'<TextNode({self.text}, {self.text_type.value}, {self.url})>'

def text_node_to_html_leaf_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.PLAINTEXT:
        return LeafNode('', text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {
            'href': text_node.url
        })
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode('img', '', {
            'src': text_node.url,
            'alt': text_node.text
        })

    else:
        raise Exception('Not an inline text type')


if __name__ == "__main__":
    result = '''<p>
This is a paragraph. It can have a lot of text inside tbh.
<b>This is bold text.</b>
This is the last sentence.
</p>'''
    md = '''This is a paragraph. It can have a lot of text inside tbh. **This is bold text.** This is the last sentence.'''
    print()