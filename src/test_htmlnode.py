import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_no_props(self):
        # Test with no properties
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        # Test the __repr__ method for correct string output
        node = HTMLNode(
            tag="p",
            value="Hello, world!",
            props={"class": "greeting"}
        )
        expected_repr = "HTMLNode(tag=p, value=Hello, world!, children=None, props={'class': 'greeting'})"
        self.assertEqual(str(node), expected_repr)

    # Tests for LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")

    def test_leaf_to_html_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
            
    def test_leaf_to_html_empty_props(self):
        node = LeafNode("span", "Hello World", {})
        self.assertEqual(node.to_html(), "<span>Hello World</span>")

    # Tests for ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_no_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "test")])

    def test_parent_node_no_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

if __name__ == "__main__":
    unittest.main()
