from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        
        props_html = ""
        for prop in self.props:
            value = self.props[prop]
            props_html += f' {prop}="{value}"'
            
        return props_html
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

    def to_html(self):
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>' 
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("A parent node must have a tag.")
        if children is None or len(children) == 0:
            raise ValueError("A parent node must have children.")
        super().__init__(tag, None, children, props)

    def to_html(self):
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError(f"Unknown text type: {text_node.text_type}")
