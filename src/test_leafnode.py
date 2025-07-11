import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    def test_to_html_a_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_to_html_cringe(self):
        node = LeafNode("cringe", "cringe_test", {"cringe": "yes", "based": "no"})
        self.assertEqual(node.to_html(), '<cringe cringe="yes" based="no">cringe_test</cringe>')
