import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    def test_props_to_html_repr_tag(self):
        node = HTMLNode(props={"href": "https://google.com", "cringe": "x.com"})
        expected = ' href="https://google.com" cringe="x.com"'
        self.assertEqual(expected, node.props_to_html())
    def test_repr(self):
        node = HTMLNode(tag="cringe", value="based")
        expected = "htmlnode: tag=cringe, value=based, children=None, props=None"
        self.assertEqual(repr(node), expected)
    def test_repr_children(self):
        node = HTMLNode(children=["gigachad", "soyface", "chudjak"])
        expected = "htmlnode: tag=None, value=None, children=['gigachad', 'soyface', 'chudjak'], props=None"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
