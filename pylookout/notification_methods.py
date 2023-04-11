from os import getenv
from urllib import request, parse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


def simple_push(hostname, notification):
    """
    Send notifications using Simplepush.
    """
    api_key = getenv("SIMPLEPUSH")
    data = parse.urlencode(
        {
            "key": api_key,
            "title": f"pyLookout on {hostname}\n",
            "msg": "\n".join(notification),
            "event": "event",
        }
    ).encode()
    req = request.Request("https://api.simplepush.io/send", data=data)
    request.urlopen(req)


def sendgrid(hostname, notification):
    """
    Send notifications using SengGrid.
    """
    api_key = getenv("SENDGRID_API_KEY")
    email_from = Email(getenv("SENDGRID_FROM"))
    email_to = To(getenv("SENDGRID_TO"))

    subject = f"pyLookout on {hostname}\n"
    content = Content("text/plain", "\n".join(notification))
    mail = Mail(email_from, email_to, subject, content)

    response = SendGridAPIClient(api_key).client.mail.send.post(
        request_body=mail.get()
    )

    return response.status_code
