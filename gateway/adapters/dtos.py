from pydantic import BaseModel, HttpUrl

class NormalizedClaims(BaseModel):
    event_type: str
    name: str
    email: str
    sub: str
    tenant_id: str
    roles: list