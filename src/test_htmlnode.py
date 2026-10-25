import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_no_prop(self):
        node1 = HTMLNode('p', 'this is a paragraph')
        output = node1.prop_to_html()
        self.assertEqual(output, '')
        
    def test_single_prop(self):
        node1 = HTMLNode('p', 'this is a paragraph', [], {'class':'paragraph'})
        output = node1.prop_to_html()
        self.assertEqual(output, 'class="paragraph"')

    def test_multiple_props(self):
        node1 = HTMLNode('p', 'this is a paragraph', [], {
            'class':'paragraph',
            'another_class': 'someotherclass'
        })
        output = node1.prop_to_html()
        self.assertEqual(output, 'class="paragraph" another_class="someotherclass"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link", {
            'href': 'www.burhan.com',
            'target': '_blank'
        })
        self.assertEqual(node.to_html(),
                         '<a href="www.burhan.com" target="_blank">Link</a>'
        )

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()