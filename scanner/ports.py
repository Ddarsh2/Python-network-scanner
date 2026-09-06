import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import PortResult
from .services import http_metadata, service_name


def _scan_one(host: str, port: int, timeout: float, http: bool) -> PortResult:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((host, port))
    except OSError:
        result = 1
    finally:
        sock.close()

    if result != 0:
        return PortResult(port=port, state="closed")

    service = service_name(port)
    status = server = None

    if http and service in {"http", "http-proxy", "https", "https-alt"}:
        tls = service in {"https", "https-alt"}
        status, server = http_metadata(host, port, timeout, use_tls=tls)

    return PortResult(
        port=port,
        state="open",
        service=service,
        http_status=status,
        http_server=server,
    )


def scan_ports(
    host: str,
    ports: list[int],
    workers: int,
    timeout: float,
    http: bool = False,
) -> list[PortResult]:
    results: list[PortResult] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_scan_one, host, port, timeout, http): port
            for port in ports
        }

        for future in as_completed(futures):
            result = future.result()
            if result.state == "open":
                results.append(result)

    return sorted(results, key=lambda r: r.port)
