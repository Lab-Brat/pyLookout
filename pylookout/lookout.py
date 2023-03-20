from os import getenv
from time import sleep
from urllib import request, parse
from .info_collector import Collector

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


class PyLookout:
    def __init__(
        self,
        threshold=75,
        method="sendgrid",
        check_containers=False,
        background=False,
    ):
        self.info = Collector(check_containers)
        self.critical = threshold
        self.method = method
        self.containers = check_containers
        self.notification = []

    def _messge_percent(self, metric, percent):
        """
        Notification message.
        """
        msg = f"Metric: {metric}\nUtilization: {percent}%\n"
        return msg

    def _simple_push(self):
        """
        Send notifications using Simplepush.
        """
        api_key = getenv("SIMPLEPUSH")
        data = parse.urlencode(
            {
                "key": api_key,
                "title": f"pyLookout on {self.info.hostname}\n",
                "msg": "\n".join(self.notification),
                "event": "event",
            }
        ).encode()
        req = request.Request("https://api.simplepush.io/send", data=data)
        request.urlopen(req)

    def _sendgrid(self):
        """
        Send notifications using SengGrid.
        """
        api_key = getenv("SENDGRID_API_KEY")
        email_from = Email(getenv("SENDGRID_FROM"))
        email_to = To(getenv("SENDGRID_TO"))

        subject = f"pyLookout on {self.info.hostname}\n"
        content = Content("text/plain", "\n".join(self.notification))
        mail = Mail(email_from, email_to, subject, content)

        response = SendGridAPIClient(api_key).client.mail.send.post(
            request_body=mail.get()
        )

        if response.status_code == 202:
            print("Email sent succsessfully!")

    def _notify(self):
        """
        Send a notification.
        Available methods:
            * local (print to console)
            * simplepush
            * sendgrid
        """
        if self.method == "local":
            print(f"pyLookout on {self.info.hostname}\n")
            for notification in self.notification:
                print(notification)
        elif self.method == "simplepush":
            self._simple_push()
        elif self.method == "sendgrid":
            self._sendgrid()

    def _containers_status(self, containers):
        """
        Check all container statuses,
        send notifications if monitored container is down.
        """
        for container in containers.values():
            if container["status"] != "running":
                name = container["name"].replace("/", "")
                self.notification.append(
                    f"CONTAINER {name} ({container['id']}) "
                    f"{container['status'].upper()}\n"
                )

    def _stressed(self, metric, percent):
        """
        Compare a metric with the critical value.
        """
        stressed = True if percent > self.critical else False

        if stressed:
            self.notification.append(self._messge_percent(metric, percent))

    def checker(self):
        """
        One by one check if CPU, RAM and Disk space
        utilization is larger than the critical value.
        """
        self._stressed("CPU", self.info.cpu_percent)
        self._stressed("RAM", self.info.ram_percent)

        for disk in self.info.disks_info.values():
            self._stressed("DISK", disk["du_percent"])

        if self.containers:
            self._containers_status(self.info.containers)

        if self.notification:
            self._notify()

    def run_in_background(self):
        """
        Run checker in background.
        """
        while True:
            self.checker()
            sleep(60)
