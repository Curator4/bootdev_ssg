import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("testnode", TextType.LINK, "http://google.com")
        node2 = TextNode("testnode", TextType.LINK, "http://x.com")
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("testnode", TextType.LINK, "http://google.com")
        node2 = TextNode("testnode", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_eq_text_type(self):
        node = TextNode("testnode", TextType.BOLD)
        node2 = TextNode("testnode", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_text(self):
        node = TextNode("testnode2", TextType.ITALIC)
        node2 = TextNode("testnode", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_text_type_enum(self):
        node = TextNode("testnode", TextType.BOLD)
        node2 = TextNode("testnode", "bold")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("click me", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click me")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("a cat", TextType.IMAGE, url="cat.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "cat.jpg", "alt": "a cat"})

if __name__ == "__main__":
    unittest.main()
