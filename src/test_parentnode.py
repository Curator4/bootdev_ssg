import unittest
from parentnode import ParentNode
from leafnode import LeafNode

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
    def test_to_html_with_multiple_children(self):
        grandchild = LeafNode("b", "grandchild")
        child_node_1 = ParentNode("span", [grandchild])
        child_node_2 = LeafNode("div", "stepchild")
        parent_node = ParentNode("div2", [child_node_1, child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<div2><span><b>grandchild</b></span><div>stepchild</div></div2>"
        )
    def test_to_html_raises_on_no_children(self):
            with self.assertRaises(ValueError) as context:
                ParentNode("div", None).to_html()
            self.assertEqual(str(context.exception), "parent node has no children")

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "main", "id": "header"})
        expected = '<div class="main" id="header"><span>child</span></div>'
        self.assertEqual(parent.to_html(), expected)

if __name__ == "__main__":
    unittest.main()
