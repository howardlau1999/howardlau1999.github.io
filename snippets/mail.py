#!/usr/bin/env python3
from email.mime.base import MIMEBase
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import os
import argparse
from email.mime.multipart import MIMEMultipart
import mimetypes
from base64 import b64encode
import json

MAILJET_API_V3 = "https://api.mailjet.com/v3/send"


def _format_addr(s):
  name, addr = parseaddr(s)
  return formataddr((Header(name, "utf-8").encode(), addr))


def _post_json(url, data, basic_auth=None):
  import urllib.request
  jsonbytes = json.dumps(data).encode("utf-8")
  req = urllib.request.Request(url, data=jsonbytes, method='POST')
  req.add_header('Content-Type', 'application/json; charset=utf-8')
  req.add_header('Content-Length', len(jsonbytes))
  if basic_auth:
    req.add_header('Authorization', f'Basic {basic_auth}')
  result = urllib.request.urlopen(req)


def mailjet(fr, to, subject, body, mime_type, attachments=None):
  url = os.getenv("MAILJET_URL") or MAILJET_API_V3
  basic_auth = b64encode(
      (os.getenv("MAILJET_AUTH") or "").encode("ascii")).decode("ascii")
  data = {
      "FromEmail": fr,
      "FromName": os.getenv("MAIL_FROM_NAME") or "howard",
      "Subject": subject,
      "To": ','.join(f"{addr.split('@')[0]} <{addr}>" for addr in to),
  }
  if mime_type == "html":
    data["Html-part"] = body
  else:
    data["Text-part"] = body
  if attachments:
    data["Attachments"] = []
    for filename in attachments:
      with open(filename, "rb") as f:
        a, b = mimetypes.guess_type(filename)
        fmime = ""
        if a is None or b is None:
          fmime = "application/octet-stream"
        else:
          fmime = f"{a}/{b}"
        data["Attachments"].append({
            "Content": b64encode(f.read()).decode("ascii"),
            "Content-type": fmime,
            "Filename": filename,
        })
  _post_json(url, data, basic_auth)


def smtp(fr, to, subject, body, mime_type, attachments=None):
  server = smtplib.SMTP_SSL(os.getenv("SMTP_HOST"),
                            os.getenv("SMTP_PORT") or 465)
  server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
  msg = MIMEMultipart()
  text = MIMEText(body, mime_type, "utf-8")
  msg['From'] = _format_addr(
      f"{os.getenv('MAIL_FROM_NAME') or 'howard'} <{fr}>")
  msg['To'] = ','.join(_format_addr(
      f"{addr.split('@')[0]} <{addr}>") for addr in to)
  msg['Subject'] = Header(subject, "utf-8").encode()
  msg.attach(text)
  if attachments:
    for i, attachment in enumerate(attachments):
      try:
        with open(attachment, "rb") as f:
          mime = MIMEBase(*mimetypes.guess_type(attachment),
                          filename=attachment)
          mime.add_header('Content-Disposition',
                          'attachment', filename=attachment)
          mime.add_header('Content-ID', f'<{i}>')
          mime.add_header('X-Attachment-Id', f'{i}')
          mime.set_payload(f.read())
          encoders.encode_base64(mime)
          msg.attach(mime)
      except:
        pass
  server.sendmail(fr or os.getenv("SMTP_USER"), to, msg.as_string())
  server.quit()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Send an email")

  parser.add_argument("--to", help="Email address to send to", required=True)
  parser.add_argument("--subject", help="Subject of the email", required=True)
  parser.add_argument("--body", help="Body of the email")
  parser.add_argument(
      "--body-file", help="Read from file the body of the email")
  parser.add_argument(
      "--html", help="Send the email as HTML", action="store_true")
  parser.add_argument("--retry", type=int, default=3,
                      help="Number of max retries")
  parser.add_argument("--attach", type=str, action="append",
                      nargs="*", help="Attatch a file")
  parser.add_argument("--via", type=str, default="smtp",
                      help="Send via SMTP or Mailgun")

  args = parser.parse_args()

  body = args.body
  if args.body_file:
    with open(args.body_file, "r", encoding="utf-8") as f:
      body = f.read()
  mime_type = "plain"
  if args.html:
    mime_type = "html"
  recipients = [addr.strip() for addr in args.to.split(",")]
  from_addr = os.getenv("MAIL_FROM")
  mail = MIMEText(body, mime_type, "utf-8")
  if args.attach:
    args.attach = [fn for arr in args.attach for fn in arr]
  if args.via == "smtp":
    smtp(from_addr, recipients, args.subject, body, mime_type, args.attach)
  elif args.via == "mailjet":
    mailjet(from_addr, recipients, args.subject, body, mime_type, args.attach)
