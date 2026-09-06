import ipaddress
import logging
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import DISCOVERY_PORTS, DEFAULT_TIMEOUT
from .models import HostResult
from .utils import resolve_hostname

log = logging.getLogger(__name__)


def _probe_host(ip: str, timeout: float) -> HostResult:
    ip_str = str(ip)

    for port in DISCOVERY_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            if sock.connect_ex((ip_str, port)) == 0:
                return HostResult(
                    ip=ip_str,
                    hostname=resolve_hostname(ip_str),
                    reachable=True,
                )
        except OSError:
            pass
        finally:
            sock.close()

    return HostResult(ip=ip_str, reachable=False)


def discover_hosts(
    network: ipaddress.IPv4Network,
    workers: int,
    timeout: float,
) -> list[HostResult]:
    hosts = list(network.hosts())
    results: list[HostResult] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(_probe_host, ip, timeout) for ip in hosts]
        for future in as_completed(futures):
            result = future.result()
            if result.reachable:
                log.info("Host reachable: %s (%s)", result.ip, result.hostname)
                results.append(result)

    return sorted(results, key=lambda r: tuple(map(int, r.ip.split("."))))
