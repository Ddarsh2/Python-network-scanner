import http.client
import socket
from typing import Optional

SERVICE_OVERRIDES = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    135: "msrpc",
    139: "netbios-ssn",
    143: "imap",
    389: "ldap",
    443: "https",
    445: "microsoft-ds",
    587: "submission",
    631: "ipp",
    993: "imaps",
    995: "pop3s",
    1433: "mssql",
    1521: "oracle",
    2049: "nfs",
    3306: "mysql",
    3389: "rdp",
    5432: "postgresql",
    5900: "vnc",
    6379: "redis",
    8080: "http-proxy",
    8443: "https-alt",
}


def service_name(port: int) -> str:
    if port in SERVICE_OVERRIDES:
        return SERVICE_OVERRIDES[port]
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def http_metadata(
    host: str,
    port: int,
    timeout: float,
    use_tls: bool = False,
) -> tuple[Optional[str], Optional[str]]:
    connection_cls = http.client.HTTPSConnection if use_tls else http.client.HTTPConnection
    conn = connection_cls(host, port=port, timeout=timeout)

    try:
        conn.request("HEAD", "/", headers={"User-Agent": "Python-Network-Scanner/1.0"})
        response = conn.getresponse()
        return str(response.status), response.getheader("Server")
    except (OSError, http.client.HTTPException):
        return None, None
    finally:
        conn.close()
