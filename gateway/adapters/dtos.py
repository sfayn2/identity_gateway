from pydantic import BaseModel, HttpUrl

class NormalizedClaims(BaseModel):
    event_type: str
    username: str
    email: str
    sub: str
    tenant_id: str
    roles: list