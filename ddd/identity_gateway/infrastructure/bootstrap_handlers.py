import os
from dotenv import load_dotenv
from ddd.order_management.infrastructure import (
    repositories,
    idp_services,
)
from ddd.identity_gateway.application import handlers

from ddd.identity_gateway.application import commands, message_bus, queries

load_dotenv()

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
#if project grows, breakdown handlers by feature

jwt_handler = access_control_services.JwtTokenHandler(
    public_key=os.getenv("KEYCLOAK_PUBLIC_KEY"),
    issuer=os.getenv("KEYCLOAK_ISSUER"),
    audience=os.getenv("KEYCLOAK_CLIENT_ID")
)


idp_provider = idp_services.KeycloakIdPProvider(
    token_url=os.getenv("KEYCLOAK_TOKEN"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET")
)

login_callback_service = idp_services.KeycloakLoginCallbackService(
    idp_provider=idp_provider,
    jwt_handler=jwt_handler,
    role_map=role_map
)



def register_command_handlers():
    message_bus.COMMAND_HANDLERS.update({
        commands.LoginCallbackCommand: lambda command: handlers.handle_login_callback(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            login_callback_service=login_callback_service
        ),
    })


def register():
    register_command_handlers()