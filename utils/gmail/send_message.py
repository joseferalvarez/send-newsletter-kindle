# utils/gmail/send_message.py

import base64
import os
from datetime import date
from email.message import EmailMessage
from googleapiclient.errors import HttpError

def send_message(service, attachments, sender, recipient):
  try:
    mime_message = EmailMessage()
  
    mime_message["To"] = recipient
    mime_message["From"] = sender
    mime_message["Subject"] = f"Newsletters of the day {date.today()}"
    mime_message.set_content("Newsletter attachments:")

    for attachment in attachments:

      filename = os.path.basename(attachment)

      with open(attachment, "rb") as file:
        data = file.read()

      mime_message.add_attachment(data, maintype="application", subtype="epub+zip", filename=filename)
  
    encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
    message = {"raw": encoded_message}
  
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=message)
        .execute()
    )

    return send_message
  except HttpError as error:
    print(error)
    send_message = None

  return send_message
