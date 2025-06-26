import unittest
from splitnodes import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "picture of ![eren](eren_link) and picture of ![mikasa](mikasa_link)"
        )
        self.assertListEqual([("eren", "eren_link"), ("mikasa", "mikasa_link")], matches)

    def test_extract_markdown_urls(self):
        text = (
            "This is a text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]

        self.assertListEqual(expected, matches)

if __name__ == "__main__":
    unittest.main()
