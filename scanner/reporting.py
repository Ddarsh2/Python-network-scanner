import csv
import json
from dataclasses import asdict
from pathlib import Path

from .models import HostResult


def write_json(path: str, results: list[HostResult]) -> None:
    output = [asdict(result) for result in results]
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2), encoding="utf-8")


def write_csv(path: str, results: list[HostResult]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "ip", "hostname", "reachable", "port", "state",
                "service", "http_status", "http_server",
            ],
        )
        writer.writeheader()

        for host in results:
            if not host.ports:
                writer.writerow({
                    "ip": host.ip,
                    "hostname": host.hostname,
                    "reachable": host.reachable,
                    "port": "",
                    "state": "",
                    "service": "",
                    "http_status": "",
                    "http_server": "",
                })
                continue

            for port in host.ports:
                writer.writerow({
                    "ip": host.ip,
                    "hostname": host.hostname,
                    "reachable": host.reachable,
                    "port": port.port,
                    "state": port.state,
                    "service": port.service,
                    "http_status": port.http_status or "",
                    "http_server": port.http_server or "",
                })
