# central_auth
central_auth : Minimal central auth gateway for Multi Context systems

A simplified, IdP-agnostic authentication service that handles login callbacks and exposes normalized /me API for use across microservices.

## Key Features
* Handles login callbacks from any OIDC compliant Idp (eg, Keycloak, Aut0, etc)
* Exposes /me endpoint w configurable info (user_id, roles, tenant_d, etc.)
* Emits user login events w configurable info?

