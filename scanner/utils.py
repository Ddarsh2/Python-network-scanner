import ipaddress
import logging
import socket


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_ports(value: str) -> list[int]:
    ports: set[int] = set()

    for part in value.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            left, right = part.split("-", 1)
            start, end = int(left), int(right)
            if start > end:
                raise ValueError("Port range start must not exceed end.")
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))

    if not ports:
        raise ValueError("No ports supplied.")

    invalid = [p for p in ports if not 1 <= p <= 65535]
    if invalid:
        raise ValueError(f"Invalid port(s): {invalid[:10]}")

    return sorted(ports)


def validate_ipv4(value: str) -> str:
    try:
        return str(ipaddress.IPv4Address(value))
    except ipaddress.AddressValueError as exc:
        raise ValueError(f"Invalid IPv4 address: {value}") from exc


def validate_network(value: str) -> ipaddress.IPv4Network:
    try:
        network = ipaddress.IPv4Network(value, strict=False)
    except ValueError as exc:
        raise ValueError(f"Invalid IPv4 network: {value}") from exc
    return network


def resolve_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, OSError):
        return "unknown"
