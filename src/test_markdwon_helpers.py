import unittest
from markdown_helpers import extract_markdown_images, extract_markdown_links

class TestMarkdownHelpers(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_extract_markdown_images_no_matches(self):
        text = "This text has no images."
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            matches,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )
    
    def test_extract_markdown_links_no_matches(self):
        text = "This text has no links."
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [])

    def test_extract_links_with_image(self):
        text = "This is an image ![image](https://i.imgur.com/zjjcJKZ.png) and a link [link](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [("link", "https://www.boot.dev")])


if __name__ == "__main__":
    unittest.main()
