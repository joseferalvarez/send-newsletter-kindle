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

    attachments_number = 0
    next_attachments = []

    for attachment in attachments:

      if attachments_number < 20:
        filename = os.path.basename(attachment)

        with open(attachment, "rb") as file:
          data = file.read()

        mime_message.add_attachment(data, maintype="application", subtype="epub+zip", filename=filename)
        attachments_number += 1
      else:
        next_attachments.append(attachment)

    encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
    message = {"raw": encoded_message}
  
    service.users().messages().send(userId="me", body=message).execute()

    if(len(next_attachments) > 1):
      send_message(service=service, attachments=next_attachments, sender=sender, recipient=recipient)

  except HttpError as error:
    print(error)
