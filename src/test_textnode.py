import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is bold text", TextType.BOLD)
        node2 = TextNode("This is bold text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_not_eq_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.example.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, None)
        self.assertEqual(repr(node), "TextNode('This is a text node', <TextType.TEXT: 'text'>, None)")
