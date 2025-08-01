from abc import ABC
from pydantic import BaseModel, constr

class Query(BaseModel, frozen=True):
    pass

class MeQuery(Query):
    tenant_id: str
    access_token: str
