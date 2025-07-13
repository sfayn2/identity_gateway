import uuid
from pydantic import BaseModel, constr
from typing import Union, List, Optional

class Command(BaseModel, frozen=True):
    token: str

class LoginCallbackCommand(Command):
    code: constr(min_length=1, strip_whitespace=True)
    redirect_uri: constr(min_length=1, strip_whitespace=True)
    next_path: constr(min_length=1, strip_whitespace=True)