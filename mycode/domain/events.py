
from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass
class DomainEvent:
    pass

class UserLoggedInEvent(Event):
    event_type: str
    sub: str
    email: str
    name: str
    tenant_id: str
    roles: list

