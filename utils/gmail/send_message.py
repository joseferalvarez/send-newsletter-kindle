# utils/gmail/send_message.py

import base64
import mimetypes
import os
from datetime import date
from email.message import EmailMessage
from email.mime.base import MIMEBase
from googleapiclient.errors import HttpError

def send_message(service, attachment, sender, recipient):
  try:
    mime_message = EmailMessage()
  
    mime_message["To"] = recipient
    mime_message["From"] = sender
    mime_message["Subject"] = f"Newsletters of the day {date.today()}"
    mime_message.set_content("Newsletter attachments:")
  
    type_subtype, _ = mimetypes.guess_type(attachment)
    maintype, subtype = type_subtype.split("/")
  
    with open(attachment, "rb") as file:
      data = MIMEBase(maintype, subtype)
      data.set_payload(file.read())
    
    filename = os.path.basename(attachment)
    data.add_header("Content-Type", type_subtype)
    data.add_header("Content-Disposition", "attachment", filename=filename)
    
    mime_message.add_attachment(data, maintype, subtype)
  
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
