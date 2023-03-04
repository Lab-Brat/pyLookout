from os import getenv
from urllib import request, parse
from info_collector import Collector


class PyLookout:
    def __init__(self, threshold=75, method="local"):
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
        Send notification using Simplepush
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

    def _notify(self, metric, percent):
        """
        Send a notification.
        Available methods:
            * local (print to console)
            * simplepush
        """
        if self.method == "local":
            print(f"Danger! ---> {metric} = {percent}")
        elif self.method == "simplepush":
            self._simple_push(metric, percent)

    def checker(self):
        """
        One by one check if CPU, RAM and Disk space
        utilization is larger than the critical value.
        """
        self._stressed("CPU", self.info.cpu_percent)
        self._stressed("RAM", self.info.ram_percent)

        for disk in self.info.disks_info.values():
            self._stressed("DISK", disk["du_percent"])
