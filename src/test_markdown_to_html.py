import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdowntoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
## This is a heading with **bold**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a heading with <b>bold</b></h2></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with **bold** and _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> and <i>italic</i></blockquote></div>",
        )


    def test_unordered_list(self):
        md = """
- Item one with _italic_
- Item two with **bold**
- Item three with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one with <i>italic</i></li><li>Item two with <b>bold</b></li><li>Item three with <code>code</code></li></ul></div>",
        )


    def test_ordered_list(self):
        md = """
1. First item
2. Second with **bold**
3. Third with _italic_ and `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second with <b>bold</b></li><li>Third with <i>italic</i> and <code>code</code></li></ol></div>",
        )


    def test_paragraph_with_link_and_image(self):
        md = """
This is a paragraph with a [link](https://example.com) and an image ![alt text](https://img.com/image.png)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a <a href="https://example.com">link</a> and an image <img src="https://img.com/image.png" alt="alt text"></p></div>',
        )
if __name__ == "__main__":
    unittest.main()
