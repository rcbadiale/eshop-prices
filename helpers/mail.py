from datetime import date

import yagmail
from credentials import PASSWORD, USERNAME


def simple_mail(subject: str, to: list, text: str):
    """
    Simple mail sender function.

    args:
        subject (str): email subject
        to (list): a list of emails
        text (str): email content (HTML / TEXT)
    """
    subject = f'[{date.today()}] {subject}'
    yagmail.SMTP(
        USERNAME,
        PASSWORD
    ).send(
        bcc=to,
        subject=subject,
        contents=text
    )
