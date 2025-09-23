import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_with_url(self):
        # This test ensures two nodes with the same properties, including URL, are equal.
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        # This test checks if nodes are correctly identified as not equal due to different URLs.
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https://blog.boot.dev")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        # This test ensures nodes with different text types are not equal.
        node = TextNode("This is bold text", TextType.BOLD_TEXT)
        node2 = TextNode("This is bold text", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        # This test verifies that different text content results in inequality.
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        # This test checks equality when one node has a URL and the other does not.
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        self.assertEqual(node, node2)
