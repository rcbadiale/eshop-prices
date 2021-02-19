from datetime import date

import yagmail

from config import EMAILS
from credentials import PASSWORD, USERNAME


def simple_mail(subject: str, text: str):
    """
    Simple mail sender function.

    args:
        subject (str): email subject
        text (str): email content (HTML / TEXT)
    """
    subject = f'[{date.today()}] {subject}'
    yagmail.SMTP(
        USERNAME,
        PASSWORD
    ).send(
        bcc=EMAILS,
        subject=subject,
        contents=text
    )
