# utils/epub/create_epub.py

from ebooklib import epub
import os

def create_epub(book, style):
  ebook = epub.EpubBook()
  ebook.set_title(book["title"])
  ebook.set_language("es")
  ebook.add_author(book["author"])
  
  book_content = epub.EpubHtml(title=book["subject"], file_name="content.xhtml", lang="es")
  book_content.content = book["content"]

  ebook.add_item(book_content)
  ebook.add_item(epub.EpubNcx())
  ebook.add_item(epub.EpubNav())

  nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
  ebook.add_item(nav_css)

  ebook.toc = (epub.Link('content.xhtml', book["subject"], 'content'),)
  ebook.spine = ['nav', book_content]

  return ebook