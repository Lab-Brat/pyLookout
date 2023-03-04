from psutil import (
    cpu_count,
    cpu_percent,
    virtual_memory as ram,
    disk_partitions,
    disk_usage,
)
from dataclasses import dataclass, field


@dataclass
class Collector:
    # CPU information
    cpu_total: str = cpu_count(logical=True)
    cpu_detail: dict = field(default_factory=dict)
    cpu_percent: str = cpu_percent()

    # RAM information
    ram_total: str = field(default_factory=str)
    ram_avail: str = field(default_factory=str)
    ram_used: str = field(default_factory=str)
    ram_percent: str = ram().percent

    # Disk information
    partitions: list = field(default_factory=list)
    disks_info: dict = field(default_factory=dict)

    def __post_init__(self):
        self.cpu_detail = {
            f"Core{i}": p for i, p in enumerate(cpu_percent(percpu=True, interval=1))
        }

        self.ram_total = self._convert_bytes(ram().total)
        self.ram_avail = self._convert_bytes(ram().available)
        self.ram_used = self._convert_bytes(ram().used)

        self.partitions = [
            part
            for part in disk_partitions()
            if "loop" not in part.device and "boot" not in part.mountpoint
        ]
        self.disks_info = self._disks_info()

    def _disks_info(self):
        """
        Get information about each individual partiion,
        except boot and loop partitions.
        """
        dd = {}
        for part in self.partitions:
            du = disk_usage(part.mountpoint)
            disk_info = {
                "du_total": self._convert_bytes(du.total),
                "du_used": self._convert_bytes(du.used),
                "du_free": self._convert_bytes(du.free),
                "du_percent": du.percent,
            }
            dd[part.device] = disk_info
        return dd

    def _convert_bytes(self, bytes, suffix="B"):
        """
        Convert bytes into human readable form
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
