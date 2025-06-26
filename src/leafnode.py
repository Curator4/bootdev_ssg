from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    def to_html(self):
        if self.value is None:
            raise ValueError("tree has no value")
        if self.tag is None:
            return self.value
        if self.tag == "img":
            return f"<img{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
