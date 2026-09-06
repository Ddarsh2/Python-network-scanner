import argparse
import ipaddress
import logging

from .config import DEFAULT_TIMEOUT, DEFAULT_WORKERS, PROFILES
from .discovery import discover_hosts
from .models import HostResult
from .ports import scan_ports
from .reporting import write_csv, write_json
from .utils import configure_logging, parse_ports, validate_ipv4, validate_network

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m scanner",
        description="Authorized IPv4 network discovery and TCP port scanner.",
    )

    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("--target", help="Single IPv4 address.")
    target_group.add_argument("--network", help="IPv4 CIDR network, e.g. 192.168.1.0/24.")

    parser.add_argument("--ports", help="Ports: 22,80,443 or ranges such as 1-1024.")
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="common",
        help="Port profile (default: common).",
    )
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--json", dest="json_path")
    parser.add_argument("--csv", dest="csv_path")
    parser.add_argument("--http", action="store_true", help="Collect basic HTTP status/Server metadata.")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
    )

    return parser


def print_results(results: list[HostResult]) -> None:
    for host in results:
        print(f"\nTarget: {host.ip}")
        print(f"Hostname: {host.hostname}")
        print(f"Status: {'reachable' if host.reachable else 'not detected'}")

        if not host.ports:
            print("No open ports found.")
            continue

        print("\nPORT     STATE   SERVICE   HTTP_STATUS   SERVER")
        print("-" * 58)

        for p in host.ports:
            print(
                f"{p.port:<8} {p.state:<7} {p.service:<9} "
                f"{(p.http_status or '-'): <13} {p.http_server or '-'}"
            )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    configure_logging(args.log_level)

    if args.workers < 1 or args.workers > 200:
        parser.error("--workers must be between 1 and 200.")

    if args.timeout <= 0 or args.timeout > 30:
        parser.error("--timeout must be > 0 and <= 30 seconds.")

    if args.ports:
        try:
            ports = parse_ports(args.ports)
        except ValueError as exc:
            parser.error(str(exc))
    else:
        ports = PROFILES[args.profile]

    results: list[HostResult] = []

    if args.target:
        try:
            target = validate_ipv4(args.target)
        except ValueError as exc:
            parser.error(str(exc))

        host = HostResult(ip=target, reachable=True)
        from .utils import resolve_hostname
        host.hostname = resolve_hostname(target)

        print(f"Scanning authorized target {target}...")
        host.ports = scan_ports(
            target, ports, args.workers, args.timeout, args.http
        )
        results = [host]

    else:
        try:
            network = validate_network(args.network)
        except ValueError as exc:
            parser.error(str(exc))

        if network.num_addresses > 1024:
            parser.error("Version 1 limits subnet discovery to 1024 addresses.")

        print(f"Discovering hosts in authorized network {network}...")
        results = discover_hosts(network, args.workers, args.timeout)

        for host in results:
            print(f"Scanning {host.ip}...")
            host.ports = scan_ports(
                host.ip, ports, args.workers, args.timeout, args.http
            )

    print_results(results)

    if args.json_path:
        write_json(args.json_path, results)
        print(f"\nJSON report: {args.json_path}")

    if args.csv_path:
        write_csv(args.csv_path, results)
        print(f"CSV report: {args.csv_path}")

    print(f"\nHosts found: {len(results)}")
    print(f"Open ports: {sum(len(h.ports) for h in results)}")
