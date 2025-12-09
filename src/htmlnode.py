#!/usr/bin/env python3

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTMLNode does not implement to_html")
    
    def props_to_html(self):
        output = ""
        if self.props is None:
            return ""
        for key, value in self.props.items():
            output += f' {key}="{value}"'
        return output
    
    def __repr__(self):
        return f'tag: {self.tag}, value: {self.value} children: {self.children} props: {self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError('LeafNode has no value')
        if not self.tag:
            return self.value
        props = self.props_to_html()
        return f'<{self.tag}{props}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('ParentNode must have a tag')
        if not self.children:
            raise ValueError('ParentNode must have children')

        output = ""
        for child in self.children:
            output += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{output}</{self.tag}>'

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"