import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
