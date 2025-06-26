import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodes(unittest.TestCase):
    def test_italic(self):
        node = TextNode("The level of _cringe_ was embarrassing", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("The level of ", TextType.TEXT),
            TextNode("cringe", TextType.ITALIC),
            TextNode(" was embarrassing", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold(self):
        node = TextNode("Eren is **free**.", TextType.TEXT)
        node2 = TextNode("But a slave to **fate**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        expected = [
            TextNode("Eren is ", TextType.TEXT),
            TextNode("free", TextType.BOLD),
            TextNode(".", TextType.TEXT),
            TextNode("But a slave to ", TextType.TEXT),
            TextNode("fate", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)

    def test_code(self):
        node1 = TextNode("Call the function `foo()`", TextType.TEXT)
        node2 = TextNode("then run `bar()`", TextType.TEXT)
        node3 = TextNode("finally `baz()` ends it.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        expected = [
            TextNode("Call the function ", TextType.TEXT),
            TextNode("foo()", TextType.CODE),
            TextNode("then run ", TextType.TEXT),
            TextNode("bar()", TextType.CODE),
            TextNode("finally ", TextType.TEXT),
            TextNode("baz()", TextType.CODE),
            TextNode(" ends it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_image_at_start_and_end(self):
        node = TextNode(
            "![start](link1) middle text ![end](link2)",
            TextType.TEXT
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "link1"),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "link2")
            ],
            result
        )

    def test_only_image_node(self):
        node = TextNode("![solo](link)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("solo", TextType.IMAGE, "link")
            ],
            result
        )


    def test_single_link_split(self):
        node = TextNode("Check this [site](example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("site", TextType.LINK, "example.com")
            ],
            result
        )

    def test_link_with_prefix_and_suffix(self):
        node = TextNode("before [link](url) after", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" after", TextType.TEXT)
            ],
            result
        )

    def test_multiple_links_in_text(self):
        node = TextNode("Click [one](1.com) or [two](2.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("one", TextType.LINK, "1.com"),
                TextNode(" or ", TextType.TEXT),
                TextNode("two", TextType.LINK, "2.com")
            ],
            result
        )

    def test_text_to_textnodes(self):
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expected)

    def test_plain_text(self):
        result = text_to_textnodes("Just a regular sentence.")
        expected = [TextNode("Just a regular sentence.", TextType.TEXT)]
        self.assertListEqual(result, expected)

    def test_only_bold(self):
        result = text_to_textnodes("**bold**")
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertListEqual(result, expected)

    def test_image_start_link_end(self):
        result = text_to_textnodes("![img](img.png) some text [click](url.com)")
        expected = [
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" some text ", TextType.TEXT),
            TextNode("click", TextType.LINK, "url.com")
        ]
        self.assertListEqual(result, expected)

    def test_adjacent_styles(self):
        result = text_to_textnodes("_italic_**bold**")
        expected = [
            TextNode("italic", TextType.ITALIC),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertListEqual(result, expected)

    def test_multiple_code_blocks(self):
        result = text_to_textnodes("`one` middle `two` end")
        expected = [
            TextNode("one", TextType.CODE),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertListEqual(result, expected)

    def test_all_formats_out_of_order(self):
        result = text_to_textnodes("[L](l) ![I](i) **B** _It_ `C`")
        expected = [
            TextNode("L", TextType.LINK, "l"),
            TextNode(" ", TextType.TEXT),
            TextNode("I", TextType.IMAGE, "i"),
            TextNode(" ", TextType.TEXT),
            TextNode("B", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("It", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("C", TextType.CODE),
        ]
        self.assertListEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
