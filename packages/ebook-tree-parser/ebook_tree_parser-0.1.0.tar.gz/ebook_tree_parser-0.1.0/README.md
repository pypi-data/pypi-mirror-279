# ebook-tree-parser

use ebooklib to parse a tree-like structure from ebooks from the TOC

## Usage

```python
from ebooklib import epub
from ebook_tree_parser.toctree import TocTree

file = "../data/frankenstein.epub"
book = epub.read_epub(file, options={'ignore_ncx': False})

estimator = lambda string: len(string)*4
tree = TocTree(book, token_estimator=estimator)

print(tree)

for node in tree3:
    print("----")
    print(f"{node.title}|{node.content_token_count}\n{node.content[:50]}")
    print("----")
```
