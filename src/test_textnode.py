import unittest
from textnode import TextNode, TextType, text_node_to_html_leaf_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node1 = TextNode('This is the first node', TextType.PLAINTEXT)
        node2 = TextNode('this is the second node', TextType.PLAINTEXT)
        self.assertNotEqual(node1, node2)

    def test_uneq_url(self):
        node1 = TextNode('This is the first node', TextType.BOLD)
        node2 = TextNode('this is the second node', TextType.PLAINTEXT, 'www.nootdev.com')
        self.assertNotEqual(node1, node2)
        

class TestNodeHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAINTEXT)
        html_node = text_node_to_html_leaf_node(node)
        # self.assertEqual(html_node.tag, 'p')  # not sure to wrap it in p or not
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")
        
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")
        
    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, 'url/to/image')
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        assert(html_node.props != None)
        self.assertEqual(html_node.props['alt'], 'This is a image node')
        self.assertEqual(html_node.props['src'], 'url/to/image')
        
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, 'url/to/link')
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'a')
        assert(html_node.props != None)
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props['href'], 'url/to/link')

if __name__ == "__main__":
    unittest.main()