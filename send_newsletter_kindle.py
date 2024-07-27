import yaml
import os
from ebooklib import epub
from bs4 import BeautifulSoup
from utils import sign_in, get_label_ids, get_message

with open("labels.yml", "r") as file:
  yml = yaml.safe_load(file)

ebooks_path = yml["path"]
service = sign_in()
labels = service.users().labels().list(userId="me").execute().get("labels", [])

selected_ids = get_label_ids(labels, yml["labels"])

for id in selected_ids:
  messages = service.users().messages().list(userId="me", labelIds=[id]).execute().get("messages", [])

  for message in messages:
    format_message = get_message(service, message_id=message["id"])

    soup = BeautifulSoup(format_message["content"], "lxml")
    
    for script in soup(["script", "style", "meta", "link"]):
      script.decompose()

    formated_content = str(soup)
    
    directory = format_message["author"].replace(" ", "")
    title = f"{format_message['subject']} - {format_message['author']}"
    
    book = epub.EpubBook()
    book.set_title(title)
    book.set_language("es")
    book.add_author(format_message["author"])
    content = epub.EpubHtml(title=format_message["subject"], file_name="content.xhtml", lang="es")
    content.content = formated_content

    book.add_item(content)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    style = '''
    body {
        font-family: Arial, sans-serif;
        line-height: 1.5;
        margin: 0;
        padding: 0;
    }
    h1, h2, h3, h4, h5, h6 {
        color: black;
    }
    p {
        margin: 1em 0;
    }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    book.toc = (epub.Link('content.xhtml', format_message["subject"], 'content'),)
    book.spine = ['nav', content]

    book_path = ebooks_path + directory
    
    if not os.path.exists(book_path):
      os.mkdir(book_path)
    
    if os.path.curdir != book_path:
      os.chdir(book_path)
    
    epub.write_epub(f"{title}.epub", book, {})