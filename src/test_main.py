
import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    
    def test_extract_title_basic(self):
        md = "# My Title\nSome paragraph text."
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_with_extra_hashes(self):
        md = "## Subtitle\n# Actual Title"
        self.assertEqual(extract_title(md), "Actual Title")

    def test_extract_title_skips_non_title_lines(self):
        md = "Paragraph\n## Subtitle\n# Title Here"
        self.assertEqual(extract_title(md), "Title Here")

    def test_extract_title_raises_when_missing(self):
        md = "No headings here.\nJust text."
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_only_uses_first(self):
        md = "# First Title\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

if __name__ == "__main__":
    unittest.main()

