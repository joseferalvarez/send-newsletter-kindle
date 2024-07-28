# utils/bsoup/format_ebook.py

from bs4 import BeautifulSoup

def format_ebook(content):
  
  soup = BeautifulSoup(content, "lxml")
  
  for script in soup(["script", "style", "meta", "link", "button", "a"]):
    script.decompose()

  return " ".join(soup.stripped_strings)