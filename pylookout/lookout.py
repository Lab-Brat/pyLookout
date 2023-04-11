import logging
from pathlib import Path
from time import sleep
from .info_collector import Collector
from .notification_methods import simple_push, sendgrid


class PyLookout:
    def __init__(
        self,
        threshold=75,
        method="local",
        check_containers=False,
    ):
        logging.basicConfig(
            format="%(asctime)s %(message)s",
            level=logging.INFO,
            handlers=[
                logging.FileHandler(f"{str(Path.home())}/.pylookout.log"),
                logging.StreamHandler(),
            ],
        )

        self.logger = logging.getLogger()
        self.info = Collector(check_containers)
        self.logger.info("Information collected successfully!")
        self.critical = threshold
        self.method = method
        self.containers = check_containers
        self.notification = []

    def _messge_percent(self, metric, percent):
        """
        Notification message.
        """
        msg = f"Metric: {metric} ===> Utilization: {percent}%"
        return msg

    def _format_message(self, stage):
        """
        Format notification message.
        """
        total_length = 66
        text_length = 24 + len(self.info.hostname)
        eq = (total_length - text_length) // 2
        return (
            f"{eq*'='}"
            f" pyLookout {stage} on {self.info.hostname} "
            f"{eq*'='}"
        )

    def _adjust_message(self):
        """
        Adjust notification message.
        """
        if self.notification != []:
            title = self._format_message("starting")
            ending = self._format_message("finished")
            self.notification.insert(0, title)
            self.notification.append(ending)

    def _notify(self):
        """
        Send a notification.
        Available methods:
            * local (print to console)
            * simplepush
            * sendgrid
        """
        self._adjust_message()
        if self.method == "local":
            [self.logger.info(line) for line in self.notification]

        elif self.method == "simplepush":
            simple_push(self.info.hostname, self.notification)
            self.logger.info("Notification sent successfully!")
            self.logger.info("Notification message:")
            [self.logger.info(line) for line in self.notification]

        elif self.method == "sendgrid":
            status_code = sendgrid(self.info.hostname, self.notification)
            if status_code == 202:
                self.logger.info("Email sent succsessfully!")
                self.logger.info("Emailed message:")
                [self.logger.info(line) for line in self.notification]

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
                    f"{container['status'].upper()}"
                )

    def _add_login_info(self):
        """
        Add login information to notification message.
        """
        if self.info.logins:
            user_ips = ""
            for login in self.info.logins:
                user_ips += f"{login['user']}->{login['ip']} "
            self.notification.append(
                f"{len(self.info.logins)} active logins: {user_ips}"
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

        self._add_login_info()

        if self.notification:
            self._notify()

    def run_in_background(self):
        """
        Run checker in background.
        """
        while True:
            self.logger.info("Running checker...")
            self.checker()
            self.logger.info("Checker finished. Sleeping for 60 seconds...")
            sleep(60)
