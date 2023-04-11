import os
import json
from psutil import (
    cpu_count,
    cpu_percent,
    virtual_memory as ram,
    disk_partitions,
    disk_usage,
)
from dataclasses import dataclass, field, InitVar


@dataclass
class Collector:
    # Containers info
    check_containers: InitVar[bool]
    containers: dict = field(default_factory=dict)

    # Hostname
    hostname: str = os.uname()[1]

    # CPU information
    cpu_total: str = cpu_count(logical=True)
    cpu_detail: dict = field(default_factory=dict)
    # do not calculate CPU usage if there is only one core
    cpu_percent: str = cpu_percent() if cpu_count() > 1 else 0

    # RAM information
    ram_total: str = field(default_factory=str)
    ram_avail: str = field(default_factory=str)
    ram_used: str = field(default_factory=str)
    ram_percent: str = ram().percent

    # Disk information
    partitions: list = field(default_factory=list)
    disks_info: dict = field(default_factory=dict)

    # Login information
    logins: list = field(default_factory=list)

    def __post_init__(self, check_containers):
        self.cpu_detail = (
            {f"Core{i}": p for i, p in enumerate(cpu_percent(percpu=True))}
            if cpu_count() > 1
            else {"Core": 0}
        )

        self.ram_total = self._convert_bytes(ram().total)
        self.ram_avail = self._convert_bytes(ram().available)
        self.ram_used = self._convert_bytes(ram().used)

        self.partitions = [
            part
            for part in disk_partitions()
            if "loop" not in part.device and "boot" not in part.mountpoint
        ]
        self.disks_info = self._disks_info()
        self.logins = self._get_logins()
        self.containers = self._get_containers() if check_containers else {}

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

    def _inspect_container(self, inspect):
        """
        Read output of 'docker compose <id>' in string format,
        return a dictionary of useful values.
        """
        return {
            "name": inspect["Name"],
            "id": inspect["Id"][0:12],
            "id_full": inspect["Id"],
            "image": inspect["Config"]["Image"],
            "created": inspect["Created"],
            "started": inspect["State"]["StartedAt"],
            "status": inspect["State"]["Status"],
            "ports": inspect["NetworkSettings"]["Ports"],
        }

    def _get_containers(self):
        """
        Get outpus of `docker ps` command,
        and parse all container information from it.
        """
        containers_parsed = {}
        docker_ps = (
            os.popen("docker ps -a | awk '{print $1}'").read().split("\n")
        )
        container_ids = docker_ps[1:-1]
        for container in container_ids:
            inspect = json.loads(
                os.popen(f"docker inspect {container}").read()
            )[0]
            container = self._inspect_container(inspect)
            containers_parsed[container["id"]] = container
        return containers_parsed

    def _get_logins(self):
        """
        Get information about current active logins.
        """
        logins = []
        logins_bash = os.popen("who").read().split("\n")
        for login in logins_bash:
            who_info = login.split()
            if who_info:
                logins.append(
                    {
                        "user": who_info[0],
                        "tty": who_info[1],
                        "date": who_info[2],
                        "time": who_info[3],
                        "ip": who_info[4][1:-1],
                    }
                )
        return logins

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
