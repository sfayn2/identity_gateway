from abc import ABC
from pydantic import BaseModel, constr

class Command(BaseModel, frozen=True):
    pass

class LoginCommand(Command):
    tenant_id: str

class LoginCallbackCommand(Command):
    tenant_id: str
    code: str

class LogoutCommand(Command):
    tenant_id: str

class RefreshTokenCommand(Command):
    tenant_id: str
    refresh_token: str