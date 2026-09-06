from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PortResult:
    port: int
    state: str
    service: str = "unknown"
    http_status: Optional[str] = None
    http_server: Optional[str] = None


@dataclass
class HostResult:
    ip: str
    hostname: str = "unknown"
    reachable: bool = False
    ports: list[PortResult] = field(default_factory=list)
