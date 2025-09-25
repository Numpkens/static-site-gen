import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "text", None, {"class": "paragraph", "href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' class="paragraph" href="https://www.example.com"')

    def test_to_html_no_tag(self):
        node = HTMLNode(None, "just text")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_to_html_no_value(self):
        node = HTMLNode("p", None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(
            "p",
            "Hello, world!",
            None,
            {"class": "greeting"}
        )
        expected_repr = "HTMLNode(tag=p, value=Hello, world!, children=None, props={'class': 'greeting'})"
        self.assertEqual(str(node), expected_repr)

    def test_leaf_to_html(self):
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")

    def test_leaf_to_html_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_parent_to_html(self):
        parent = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                LeafNode("p", "Paragraph one."),
                LeafNode("p", "Paragraph two.")
            ],
        )
        expected_html = "<div><h1>Title</h1><p>Paragraph one.</p><p>Paragraph two.</p></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_no_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "paragraph")]).to_html()

    def test_parent_node_no_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()
