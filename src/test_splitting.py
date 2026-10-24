import unittest
from splitting import *
from textnode import *


class TestAllSplitting(unittest.TestCase):
    def test_all_splitting(self):
        output = text_to_textnodes('This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)')
        self.assertEqual(output, [
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

class TestSplitting(unittest.TestCase):
    def test_plaintext_nodel(self):
        node1 = TextNode('This is a string of plaintext', TextType.PLAINTEXT)
        output = split_nodes_delimiter([node1], '`', TextType.CODE)
        self.assertEqual(len(output), 1, 'same length when no inline element')
        self.assertEqual(output[0].text, node1.text, 'same text - no change')
        self.assertEqual(output[0].text_type, TextType.PLAINTEXT)

    def test_other_types(self):
        bold = TextNode('This is bold string `this will not be splitted` and this as well', TextType.BOLD)
        italic = TextNode('This is italic string **this will not be splitted** and this as well', TextType.ITALIC)
        code = TextNode('This is code string _this will not be splitted_ and this as well', TextType.CODE)
        for node, delimiter in [bold, '`'], [italic, '**'], [code, '_']:
            output = split_nodes_delimiter([node], delimiter, TextType.LINK) # whatever the type is it should not split 
            self.assertEqual(len(output), 1, 'no splitting only returning - because not plaintext')

    def test_plaintest_inline(self, delimiter='`', texttype = TextType.CODE):
        node = TextNode(f'This is plain string {delimiter}this will be splitted{delimiter} and this as well', TextType.PLAINTEXT)
        output = split_nodes_delimiter([node], delimiter, texttype)
        self.assertEqual(len(output), 3, 'must contain two plain nodes and one code node')
        self.assertEqual(output[1].text_type, texttype)
        self.assertEqual(output[1].text, 'this will be splitted', 'text in node is correct without delimiter')
        self.assertEqual(output[0].text, 'This is plain string ', 'must not contain delimiter and have leading space')
        self.assertEqual(output[2].text, ' and this as well', 'must not contain delimiter and have leading space in start')

    def test_other_types_inline(self):
        self.test_plaintest_inline('*', TextType.BOLD)
        self.test_plaintest_inline('_', TextType.ITALIC)


# work for findall method in extract_markdown functions
# class TestMdExtract(unittest.TestCase):
#     def test_extract_markdown_images(self):
#         matches = extract_markdown_images(
#             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
#         )
#         self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

#     def test_extract_markdown_links(self):
#         matches = extract_markdown_links(
#             "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
#         )
#         self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestLinkSplitting(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAINTEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAINTEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAINTEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
            node = TextNode(
                "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
                TextType.PLAINTEXT,
            )
            new_nodes = split_nodes_link([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.PLAINTEXT),
                    TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.PLAINTEXT),
                    TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                ],
                new_nodes,
            )