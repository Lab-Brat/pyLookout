from info_collector import Collector


class PyLookout:
    def __init__(self, threshold=80):
        self.info = Collector()
        self.critical = threshold

    def _stressed(self, metric, percent):
        """
        Compare a metric with the critical value.
        """
        stressed = True if percent > self.critical else False

        if stressed:
            self._notify(metric, percent)

    def _notify(self, metric, percent):
        """
        Send a notification.
        (right now it's just a print statement).
        """
        print(f"Danger! ---> {metric} = {percent}")

    def checker(self):
        """
        One by one check if CPU, RAM and Disk space
        utilization is larger than the critical value.
        """
        self._stressed("CPU", self.info.cpu_percent)
        self._stressed("RAM", self.info.ram_percent)

        for disk in self.info.disks_info.values():
            self._stressed("DISK", disk["du_percent"])
