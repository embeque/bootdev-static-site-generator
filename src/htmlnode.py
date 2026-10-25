class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag: str|None = tag
        self.value: str|None = value
        self.children: list[HTMLNode]|None = children
        self.props: dict[str, str]|None = props

    def to_html(self):
        raise NotImplementedError('Method must be overriden by the child classes')

    def prop_to_html(self) -> str:
        if self.props is None:
            return ''

        result = ''
        for key, value in self.props.items():
            result += f'{key}="{value}" '
        return result.strip()

    def __repr__(self) -> str:
        return f'<{self.tag}: {self.value} -props {self.props} -child ({self.children})>'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError('All leaf nodes must have a value')
        elif self.tag == None:
            return self.value

        if self.tag == 'p':
            return self.value
        
        before_prop = f'<{self.tag}'
        after_prop = f'>{self.value}</{self.tag}>'

        props_html = self.prop_to_html()
        if props_html != '':
            before_prop += f' {props_html}'

        return before_prop + after_prop

    def __repr__(self) -> str:
        return f'<{self.tag}: {self.value} - {self.props}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        # print(f'inparent children:{children}  ')
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError('Parent Node must have a tag')
        if not self.children:
            raise ValueError('Parent Node must have at least one children')

        open_tag = f'<{self.tag}>'
        close_tag = f'</{self.tag}>'

        content = ''
        for child in self.children:
            content += child.to_html()

        return open_tag + content + close_tag

    