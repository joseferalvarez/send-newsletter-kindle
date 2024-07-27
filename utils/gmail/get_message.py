# utils/get_label_messages.py

import base64

def get_message(service, message_id):
    content = service.users().messages().get(userId="me", id=message_id, format="full").execute()
    format_message = {}

    payload = content["payload"]
    headers = payload.get("headers")
    parts = payload.get("parts")
    body = None

    if parts:
      for part in parts:
        body = part["body"].get("data")
        if body:
          body = base64.urlsafe_b64decode(body).decode("utf-8")
    if not body:
      body = payload["body"].get("data")
      if(body):
          body = base64.urlsafe_b64decode(body).decode("utf-8")
    
    for header in headers:
      if header["name"] == "Subject":
        format_message["subject"] = header["value"]
      if header["name"] == "Date":
        format_message["date"] = header["value"]
      if header["name"] == "From":
        format_message["author"] = header["value"].split(" <")[0]

    format_message["content"] = body

    return format_message
