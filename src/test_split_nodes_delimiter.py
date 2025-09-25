import unittest
from textnode import TextNode, TextType
from markdown_helpers import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is a **bold** and **another** test.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
            TextNode(" test.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_italic(self):
        node = TextNode("This is a *italic* test.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" test.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_code(self):
        node = TextNode("This is a `code` test.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" test.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_with_multiple_delimiters(self):
        node = TextNode("This has `code`, **bold**, and *italic* text.", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_no_delimiter_present(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [TextNode("This is just plain text.", TextType.TEXT)]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_invalid_syntax(self):
        node = TextNode("This is **invalid markdown.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
