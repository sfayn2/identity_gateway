from __future__ import annotations
from typing import Union
from ddd.identity_gateway.application import (
    commands, 
    ports, 
    dtos, 
)
from ddd.identity_gateway.domain import exceptions

def handle_login_callback(
        command: commands.LoginCallbackCommand, 
        uow: UnitOfWorkAbstract, 
        login_service: IdPCallbackServiceAbstract
    ) -> dtos.IdPTokenDTO:

    tokens = login_callback_service.get_tokens(command.code, command.redirect_uri)

    return tokens