# central_auth
central_auth : Minimal central auth gateway for Multi Context systems

A simplified, IdP-agnostic authentication service that handles login callbacks and exposes normalized /me API for use across microservices.

## Key Features
* Handles login callbacks from any OIDC compliant Idp (eg, Keycloak, Aut0, etc)
* Exposes /me endpoint w configurable info (user_id, roles, tenant_d, etc.)
* Emits user login events w configurable info?

## Why Use this

In a module or microservice-based system ecach context (Order management, product catalog, etc)
need user identity and access info. Instead of letting every service parse and verify IdP Tokens;

Let central_auth handle login once, normalize claims, and serve consistent user info via /me

This approach:
* Reduces duplication across services
* Avoids tigh coupling to any specific IdP


### Example flow
1. Frontend logs in via Keycloack/Auth0
2. Redirects to central_auth/login/callback
3. central_auth
   * Verifieds token
   * Extracts normalized claims
   * Stores user (or emits event)
4. Any context (e.g Order) calls /me to get identity info like
   ```json
   {
   {
    "sub": "abc123",
    "email": "abc@email.com",
    "tenant_id": "tenant-abc",
    "realm_access": {
        "roles": ["customer"]
    },
    "vendor_id": "v-124",
    "vendor_name": "vendor 1",
    "vendor_country": "India",
    "shipping_address": {
        "street": "123 Main st",
        "city": "Metro city",
        "state": "Stat1",
        "postal": 1234,
        "country": "IX"
    }
}
   }
   ```

