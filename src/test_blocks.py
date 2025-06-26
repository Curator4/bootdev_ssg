import unittest
from blocks import markdown_to_blocks, BlockType, block_to_block_type

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ],
        )

    def test_markdown_to_blocks_aot(self):
        md = """
# main characters

**Eren**, the main character

_Mikasa_, the female lead

`Armin`, the smart best friend

in a list they are:

- Eren
- Mikasa
- Armin
- Floch
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# main characters",
                "**Eren**, the main character",
                "_Mikasa_, the female lead",
                "`Armin`, the smart best friend",
                "in a list they are:",
                "- Eren\n- Mikasa\n- Armin\n- Floch",
            ],
        )

    def test_block_to_block_type_heading(self):
        block = "#### The Industrial Revolution and its Consequences"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\ndef add(x, y):\n    return x + y\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote.\n> Still quoted.\n> Even this line."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- Eggs\n- Milk\n- Bread"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. Wake up\n2. Code\n3. Sleep"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "The quick brown fox jumps over the lazy dog."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_no_space(self):
        block = "##This is not a heading"  # No space after ##
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        block = "####### Too many hashes"  # 7 hashes — invalid
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_with_only_opening_backticks(self):
        block = "```\ndef hello():\n    pass"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_with_one_line_not_quoted(self):
        block = "> Line one\nThis is not quoted\n> Line three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_with_missing_dash(self):
        block = "- Item one\nNot a list item\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_with_wrong_numbering(self):
        block = "1. First\n3. Skipped a number\n4. Still wrong"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_with_missing_dot(self):
        block = "1 First item\n2 Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
