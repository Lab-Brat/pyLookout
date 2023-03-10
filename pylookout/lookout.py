from os import getenv
from urllib import request, parse
from .info_collector import Collector

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


class PyLookout:
    def __init__(self, threshold=75, method="sendgrid"):
        self.info = Collector()
        self.critical = threshold
        self.method = method

    def _stressed(self, metric, percent):
        """
        Compare a metric with the critical value.
        """
        stressed = True if percent > self.critical else False

        if stressed:
            self._notify(metric, percent)

    def _simple_push(self, metric, percent):
        """
        Send notifications using Simplepush.
        """
        api_key = getenv("SIMPLEPUSH")
        data = parse.urlencode(
            {
                "key": api_key,
                "title": "pyLookout!",
                "msg": f"Danger! ---> {metric} = {percent}",
                "event": "event",
            }
        ).encode()
        req = request.Request("https://api.simplepush.io/send", data=data)
        request.urlopen(req)

    def _sendgrid(self, metric, percent):
        """
        Send notifications using SengGrid.
        """
        api_key = getenv("SENDGRID_API_KEY")
        email_from = Email(getenv("SENDGRID_FROM"))
        email_to = To(getenv("SENDGRID_TO"))

        subject = "pyLookout notifications"
        content = Content("text/plain", f"Danger! ---> {metric} = {percent}")
        mail = Mail(email_from, email_to, subject, content)

        response = SendGridAPIClient(api_key).client.mail.send.post(
            request_body=mail.get()
        )

        if response.status_code == 202:
            print("Email sent succsessfully!")

    def _notify(self, metric, percent):
        """
        Send a notification.
        Available methods:
            * local (print to console)
            * simplepush
            * sendgrid
        """
        if self.method == "local":
            print(f"Danger! ---> {metric} = {percent}")
        elif self.method == "simplepush":
            self._simple_push(metric, percent)
        elif self.method == "sendgrid":
            self._sendgrid(metric, percent)

    def _containers_status(self, containers):
        """
        Check all container statuses,
        send notifications if monitored container is down.
        """
        for container in containers.values():
            if container["status"] != "running":
                name = container["name"].replace("/", "")
                self._notify(
                    f"CONTAINER {name} ({container['id']})",
                    container["status"].upper(),
                )

    def checker(self):
        """
        One by one check if CPU, RAM and Disk space
        utilization is larger than the critical value.
        """
        self._stressed("CPU", self.info.cpu_percent)
        self._stressed("RAM", self.info.ram_percent)

        for disk in self.info.disks_info.values():
            self._stressed("DISK", disk["du_percent"])

        self._containers_status(self.info.containers)


def main():
    threshold = 75
    notification_method = "local"
    lk = PyLookout(threshold, notification_method)
    lk.checker()


if __name__ == "__main__":
    main()
