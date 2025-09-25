import unittest
from markdown_helpers import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image,
    split_nodes_link,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title
)
from textnode import TextNode, TextType
from block_type import BlockType
from htmlnode import ParentNode, LeafNode

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
        text = "This is an image ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to Boot.dev](https://boot.dev)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [("to Boot.dev", "https://boot.dev")]
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
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
                TextNode(" here", TextType.TEXT)
            ],
            nodes_with_images_and_links
        )

class TestMarkdownToBlocks(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "This is **bolded** paragraph\ntext in a p\ntag here",
                "This is another paragraph with _italic_ text and `code` here",
            ],
            blocks,
        )

    def test_codeblock(self):
        md = """ 
This is text that should remain
the same even with inline stuff

"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual([md.strip()], blocks)

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_no_space(self):
        block = "##heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_heading_too_many_hashes(self):
        block = "####### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
    def test_quote_multiple_lines(self):
        block = "> This is a quote\n> with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
    def test_quote_multiple_lines_with_whitespace(self):
        block = ">This is a quote\n>  with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_code(self):
        block = "```\ndef some_code():\n  pass\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_unordered_list(self):
        block = "* First item\n* Second item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
    def test_unordered_list_dashes(self):
        block = "- First item\n- Second item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_with_skipped_number(self):
        block = "1. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_ordered_list_wrong_start_number(self):
        block = "2. First item\n3. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_ordered_list_single_line(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        
    def test_mixed_list_types(self):
        block = "1. An item\n* Another item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_mixed_heading_and_paragraph(self):
        block = "# heading\nThis is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
class TestMarkdownToHTMLNode(unittest.TestCase):
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
        md = "```\ndef some_code():\n  pass\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\ndef some_code():\n  pass\n</code></pre></div>",
        )
    
    def test_quote(self):
        md = "> A quote\n> with multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>A quote with multiple lines</blockquote></div>"
        )
    
    def test_ul(self):
        md = "* Item 1\n* Item 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        )
        
    def test_ol(self):
        md = "1. Item 1\n2. Item 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li></ol></div>"
        )

    def test_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )
        
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

    def test_extract_title_whitespace(self):
        markdown = """ # This is a title with whitespace """
        self.assertEqual(extract_title(markdown), "This is a title with whitespace")
