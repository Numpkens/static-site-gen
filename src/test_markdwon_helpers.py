import unittest
from markdown_helpers import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image,
    split_nodes_link,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title,
    split_nodes_delimiter,
    text_to_textnodes
)
from textnode import TextNode, TextType
from block_type import BlockType
from htmlnode import ParentNode, LeafNode, text_node_to_html_node

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

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    def test_split_nodes_link_and_image_interspersed(self):
        node = TextNode(
            "this is text with an [link](https://www.example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png) here", 
            TextType.TEXT
        )
        nodes_with_links = split_nodes_link([node])
        nodes_with_images_and_links = split_nodes_image(nodes_with_links)
        self.assertListEqual(
            [
                TextNode("this is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" here", TextType.TEXT),
            ],
            nodes_with_images_and_links,
        )
        
    def test_split_nodes_image_and_link_reversed(self):
        node = TextNode(
            "this is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.example.com) here", 
            TextType.TEXT
        )
        nodes_with_images = split_nodes_image([node])
        nodes_with_links_and_images = split_nodes_link(nodes_with_images)
        self.assertListEqual(
            [
                TextNode("this is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" here", TextType.TEXT),
            ],
            nodes_with_links_and_images,
        )

    def test_split_nodes_delimiter_bold(self):
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

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is a `code` test.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" test.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is a *italic* test.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" test.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("This is a **bold test.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_markdown_to_blocks_with_newlines(self):
        markdown = "This is a paragraph.\n\nThis is another paragraph."
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, ["This is a paragraph.", "This is another paragraph."])

    def test_markdown_to_blocks_with_extra_whitespace(self):
        markdown = "  This is a paragraph.  \n\n  \n\nThis is another paragraph."
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, ["This is a paragraph.", "This is another paragraph."])
        
    def test_heading_no_space(self):
        block = "#This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_mixed_heading_and_paragraph(self):
        block = "# Heading\n\nThis is a paragraph."
        blocks = markdown_to_blocks(block)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)

    def test_block_to_block_type(self):
        test_cases = [
            ("# Heading", BlockType.HEADING),
            ("## Another Heading", BlockType.HEADING),
            ("```\nprint('hello')\n```", BlockType.CODE),
            ("> This is a quote\n> with two lines", BlockType.QUOTE),
            ("* This is a list item\n* Another list item", BlockType.UNORDERED_LIST),
            ("1. First item\n2. Second item", BlockType.ORDERED_LIST),
            ("This is a regular paragraph.", BlockType.PARAGRAPH),
        ]
        
        for block, expected_type in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected_type)
    
    def test_markdown_to_html_node_paragraph(self):
        md = "This is a **bold** paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a <b>bold</b> paragraph.</p></div>")

    def test_markdown_to_html_node_headings(self):
        md = "# H1\n\n## H2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>H1</h1><h2>H2</h2></div>")
        
    def test_markdown_to_html_node_ul(self):
        md = "* list item 1\n* list item 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>list item 1</li><li>list item 2</li></ul></div>")

    def test_markdown_to_html_node_ol(self):
        md = "1. list item 1\n2. list item 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>list item 1</li><li>list item 2</li></ol></div>")

    def test_extract_title(self):
        markdown = """# This is a title

This is a paragraph.
        """
        self.assertEqual(extract_title(markdown), "This is a title")

    def test_extract_title_no_h1(self):
        markdown = """
## This is a heading
This is a paragraph.
        """
        with self.assertRaises(Exception):
            extract_title(markdown)
