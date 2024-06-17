from collections import defaultdict
from typing import Literal,Callable
from itertools import zip_longest

from ebooklib import epub

from bs4 import BeautifulSoup
from bs4.element import Tag

import html2text
H2T = html2text.HTML2Text()
H2T.body_width = 0

try:
    import tiktoken
    
except ImportError:
    pass

def GET_ESTIMATOR(source: str, encoding_name:str='cl100k_base') -> Callable[[str], int]:
        """Use the tiktoken library to estimate the number of tokens in a text.
        See [tiktoken](https://github.com/openai/tiktoken) for more information. 

        Args:
            source (str): Source of the estimator. I.e. "openai" or "tiktoken" for the tiktoken library.
            encoding_name (str, optional): The tiktoken encoding name used to count and estimate the number of tokens. Defaults to 'cl100k_base'.

        Returns:
            Callable[[str], int]: A function that takes a string and returns the number of tokens in the string.
        """
        try:
            if source.lower() == 'openai' or source.lower() == 'tiktoken':
                encoding = tiktoken.get_encoding(encoding_name=encoding_name)
                return lambda x: len(encoding.encode(x))
        except ImportError:
            pass
    
def has_text(tag):
    return tag.string is not None and tag.string.strip()

def is_link(element: Tag) -> bool:
    return element.name == 'a'

def only_link_content(element: Tag) -> bool:
    if element.name == 'a':
        return True
    if not hasattr(element, 'contents'):
        return False
    return all(is_link(child) for child in element.contents)

def elem_contains_element(elem: Tag, other_elem: Tag | None) -> bool:
    """Check if elem contains other_elem. Will return True if elem == other_elem.

    Args:
        elem (Tag): The first element.
        elem2 (Tag | None): The second element.

    Returns:
        bool: True if elem1 contains elem2.
    """
    if other_elem is None:
        return False
    
    if elem == other_elem:
        return True
    
    if elem.find(other_elem.name, attrs=other_elem.attrs) is not None:
        return True
    return False

def find_parent_sibling(elem: Tag, dir: Literal['next', 'previous'] = 'next') -> Tag:
    """Find the next/previous parent sibling of the element. If the element has no parent sibling, will return None.

    Args:
        elem (Tag): The element to find the next parent sibling of.
        direction (Literal['next', 'previous'], optional): The direction to search. Defaults to 'next'.

    Returns:
        Tag: The next/previous parent sibling of the element.
    """
    if elem is None:
        return None
    
    if elem.parent is None:
        return None
    
    if dir == 'previous':
        parent_sibling = elem.parent.find_previous_sibling()
    else: # default to next
        parent_sibling = elem.parent.find_next_sibling()
    
    if parent_sibling is None:
        return find_parent_sibling(elem.parent, dir=dir)
    else:
        return parent_sibling
    
def _extract_content_before_elem(elem: Tag) -> list[str]:
    """Extract the content before an element. Will only include text, not links.

    Args:
        elem (Tag): The element to extract the content before.

    Returns:
        list[str]: The extracted content. Will be in reverse order of appearance.
    """
    if elem is None:
        return []
    
    content_list = []
    current_element = elem
    
    while current_element:
        
        previous_sibling = current_element.find_previous_sibling()
        if previous_sibling is None: # if there is no previous sibling, go to the parent
            current_element = find_parent_sibling(current_element, dir='previous')
            if current_element is None:
                return content_list
        else:
            current_element = previous_sibling
            
        if not only_link_content(current_element): # if there is only content that is a link
            if current_element.text.strip() != "":
                content_list.append(H2T.handle(str(current_element)))

    return content_list

def extract_content_between_elems(elem1: Tag, elem2: Tag) -> list[str]:
    """Extract the content between two elements. Will include elem1, but not elem2. Will only include text, not links.

    Args:
        elem1 (Tag): The first element.
        elem2 (Tag): The second element.

    Returns:
        list[str]: The extracted content.
    """
    if elem1 is None and elem2 is None:
        return []
    
    if elem1 is None:
        return _extract_content_before_elem(elem2)[::-1]
    
    content_list = []
    current_element = elem1
    
    while current_element:
        if current_element == elem2: # if we reach the second element, stop
            return content_list
        
        if elem_contains_element(current_element, elem2): # if the second element is inside the current element, then we need to go into the children of the current element
            return extract_content_between_elems(current_element.find_next(), elem2)
        
        if not only_link_content(current_element): # if there is only content that is a link
            if current_element.text.strip() != "":
                content_list.append(H2T.handle(str(current_element)))

        next_sibling = current_element.find_next_sibling()
        if next_sibling is None:
            current_element = find_parent_sibling(current_element, dir='next')
            if current_element is None:
                return content_list
        else:
            current_element = next_sibling

    return content_list
    
def split_href(href:str) -> tuple[str, str]:
    """
    Split the href into the link and the anchor (if it exists)
    """
    
    if '#' in href:
        return href.split('#')
    else:
        return href, None
    
def get_soup(book: epub.EpubBook, href:str) -> BeautifulSoup:
    content = book.get_item_with_href(href).get_body_content()
    try:
        return BeautifulSoup(content, 'lxml')
    except ImportError: # lxml not installed
        try:
            return BeautifulSoup(content, 'html5lib')
        except ImportError: # html5lib not installed
            return BeautifulSoup(content, 'html.parser')
    except:
        return BeautifulSoup(content, 'html5lib')

class TocNode(dict):
    def __init__(self, title:str='', href:str='', anchor:str='', level:int=0, children:list=None):
        self.title = title
        self.href = href
        self.anchor = anchor
        self.level = level
        self.children: list[TocNode] = children
        self.element: BeautifulSoup = None
        self.content: str = None
        self.content_token_count: int = None
    
    def set_children(self, children: list):
        self.children = children
    
    def get_children(self) -> list:
        return self.children
    
    def get_num_children(self) -> int:
        if not self.children:
            return 0
        return len(self.children)
    
    def is_leaf(self) -> bool:
        return not bool(self.children)
    
    def is_root(self) -> bool:
        return self.level <= 0
    
    def get_item_with_href(self, book:epub.EpubBook) -> BeautifulSoup:
        book.get_item_with_href(self.href)
    
    def soup_element(self, soup: BeautifulSoup) -> Tag:
        if self.anchor:
            self.element = soup.find(id=self.anchor)
            return self.element
        else:
            self.element = soup.find(has_text) # find the first element with text
            return self.element
    
    def set_content(self, content: str, token_estimator: Callable[[str], int] = None):
        self.content = content
        if token_estimator: self.content_token_count = token_estimator(content)
        
    def set_tok_count(self, token_estimator: Callable[[str], int]):
        if token_estimator: self.content_token_count = token_estimator(self.content)
        
    def get_section_tok_count(self) -> int:
        tok_count = 0
        for child in self.children:
            tok_count += child.get_section_tok_count()
            
        return tok_count + self.content_token_count
    
    def __repr__(self):
        return f"title={self.title}, href={self.href}#{self.anchor if self.anchor else ''}, level={self.level}, #children={self.get_num_children()}"
    
    def __str__(self):
        return f"title={self.title}, href={self.href}#{self.anchor if self.anchor else ''}, level={self.level}, #children={self.get_num_children()}"
    
    def __iter__(self):
        return iter(self.children)
    
    def __next__(self):
        return next(self.children)
    
    def __getitem__(self, key):
        return self.children[key]
    
class TocTree:
    
    def __init__(self, book: epub.EpubBook, token_estimator: Callable[[str], int] = None):
        """Tree structure of the Table of Contents of an Epub book and the content of each node.

        Args:
            book (epub.EpubBook): Epub book object
            token_estimater (Callable[[str], int], optional): Function to estimate the number of tokens in a string. Defaults to None.
        """

        self.token_estimator = token_estimator
        self.book = book
        
        self.root: TocNode = TocNode('root')
        self._parse_toc_tree(self.root, book.toc)
        self.inorder: list[TocNode] = self._get_inorder(self.root, [])[1:] # without the root node
        """list of nodes in the order they will appear in the book. The first element is the root node, so it is removed. Technically preorder traversal.
        Iterating on TocTree will iterate over this list."""
        
        self._href_soup_cache: dict[str, BeautifulSoup] = dict()
        """cache of different html files in the book. The key is the href of the file"""
        self._href_node_cache: dict[str, list[TocNode]] = defaultdict(list)
        """cache of nodes that have the same href. The key is the href of the file"""
        
        for node in self.inorder:
            if node.href and node.href not in self._href_soup_cache:
                self._href_soup_cache[node.href] = get_soup(book, node.href)
            self._href_node_cache[node.href].append(node)
        
        for href, nodes in self._href_node_cache.items():
            if len(nodes) == 1: # if there are multiple nodes with the same href, then we need to combine them
                nodes[0].set_content(H2T.handle(self._href_soup_cache[href].prettify()), token_estimator=self.token_estimator)
            else: # if there is only 1 node with the href, then we need to set the content of the node
                self._set_xhtml_content(nodes)
    
    def _parse_toc_tree(self, toc_node:TocNode, toc_list:list) -> list:
        next_toc_list = []

        for entry in toc_list:
            if isinstance(entry, tuple):
                section, nested_toc = entry
                section : epub.Section
                nested_toc : list
                href, anchor = split_href(section.href)

                tmp_node = TocNode(title=section.title, href=href, anchor=anchor, level=toc_node.level+1)
                next_toc_list.append(tmp_node)
                self._parse_toc_tree(tmp_node, nested_toc)
                
            elif isinstance(entry, epub.Link):
                href, anchor = split_href(entry.href)
                next_toc_list.append(TocNode(title=entry.title, href=href, anchor=anchor, level=toc_node.level+1))
                
        toc_node.set_children(next_toc_list)
        return toc_node
    
    def _get_inorder(self, toc_node:TocNode, inorder:list) -> list:
        inorder.append(toc_node)
        
        if not toc_node.is_leaf():
            for child in toc_node.get_children():
                self._get_inorder(child, inorder)
                
        return inorder
    
    def _set_xhtml_content(self, node_list:list[TocNode]) -> str:
        """Set the content of the nodes in the list. Will combine the content between the nodes.

        Args:
            node_list (list[TocNode]): List of nodes to set the content of.

        Returns:
            str: The combined content of the nodes.
        """
        first_node = True
        for node1, node2 in zip_longest(node_list, node_list[1:]):
            elem1 = self.get_soup_element(node1)
            elem2 = self.get_soup_element(node2)
            if first_node:
                first_node = False
 
                content = "\n".join(extract_content_between_elems(None, elem1) + extract_content_between_elems(elem1, elem2))
                node1.set_content(content, token_estimator=self.token_estimator)
            else:
                content = "\n".join(extract_content_between_elems(elem1, elem2))
                node1.set_content(content, token_estimator=self.token_estimator)
    
    def get_tree(self) -> TocNode:
        return self.root
    
    def get_inorder(self) -> list:
        return self.inorder
    
    def get_item_with_href(self, href:str) -> BeautifulSoup:
        if self._href_soup_cache[href]:
            return self._href_soup_cache[href]
        else:
            return get_soup(self.book, href)
    
    def get_soup_element(self, node:TocNode | None) -> Tag:
        if node is None:
            return None
        return node.soup_element(self.get_item_with_href(node.href))
    
    def update_encoding(self, encoding_name: str):
        self.encoding = tiktoken.get_encoding(encoding_name=encoding_name)
        for node in self.inorder:
            node.set_tok_count(self.encoding)
    
    def __iter__(self):
        return iter(self.inorder)
    
    def __next__(self):
        return next(self.inorder)
    
    def __getitem__(self, key) -> TocNode:
        return self.inorder[key]
        
    def __repr__(self) -> str:
        return f"TOC Tree: {self.root}"
    
    def __str__(self) -> str:
        return f"TOC Tree: {self.root}"