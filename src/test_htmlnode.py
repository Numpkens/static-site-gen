import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
