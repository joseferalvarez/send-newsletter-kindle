import yaml
import os
from ebooklib import epub
from utils import sign_in, get_label_ids, get_message, format_ebook, create_epub, send_message

EBOOK_CSS_PATH = os.path.abspath("./utils/epub/style.css")

with open("labels.yml", "r") as file:
  yml = yaml.safe_load(file)

with open(EBOOK_CSS_PATH, "r") as file:
  style = file.read()

unsended_ebooks = []

ebooks_path = yml["path"]
service = sign_in()
labels = service.users().labels().list(userId="me").execute().get("labels", [])

selected_ids = get_label_ids(labels, yml["labels"])

for id in selected_ids:
  message_ids = service.users().messages().list(userId="me", labelIds=[id]).execute().get("messages", [])

  for message_id in message_ids:
    message = get_message(service, message_id=message_id["id"])
    book = {}

    message_date = message["date"].split(" ")
    date_text = " ".join([message_date[1], message_date[2], message_date[3]])

    book["title"] = f"{message['subject']} - {message['author']} - {date_text}"
    book["author"] = message["author"]
    book["subject"] = message["subject"]
    book["content"] = format_ebook(message["content"])

    epub_book = create_epub(book, style)

    author_directory = message["author"].replace(" ", "") + "/"

    folder_path = ebooks_path + author_directory
    book_path = f"{folder_path}{book['title']}.epub"

    if not os.path.exists(book_path):
      print(f"The ebook {book['title']} dont exist, saving ebook...")
      if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Folder {author_directory} created")
      if os.path.curdir != folder_path:
        os.chdir(folder_path)
      
      epub.write_epub(f"{book['title']}.epub", epub_book, {})
      print(f"The ebook {book['title']} was saved succesfully")

      unsended_ebooks.append(book_path)
    else:
      print(f"The ebook {book['title']} already exists")


if len(unsended_ebooks) > 0:
  send_message(service, unsended_ebooks, yml["sender"], yml["recipient"])