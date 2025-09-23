import unittest

from textnode import TextNode, TextType, split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_single_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_multiple_code(self):
        node = TextNode("This is `a code` block with `another` one", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("a code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" block with ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("another", TextType.CODE))
    
    def test_split_bold(self):
        node = TextNode("This is text with **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD_TEXT))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC_TEXT))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_unbalanced_delimiter(self):
        node = TextNode("This is `a code block without a closing delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
            
    def test_split_no_delimiter(self):
        node = TextNode("This is just normal text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This is just normal text", TextType.TEXT))
        
    def test_split_on_non_text_node(self):
        node = TextNode("This is bold text", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This is bold text", TextType.BOLD_TEXT))


if __name__ == "__main__":
    unittest.main()
