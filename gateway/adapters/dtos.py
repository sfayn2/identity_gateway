from pydantic import BaseModel, HttpUrl

class NormalizedClaims(BaseModel):
    event_type: str
    sub: str
    tenant_id: str
    roles: list