# identity_gateway
identity_gateway : A lightweight **Identity Gateway** that centrally handles login callback from  any selected IDPs (Keycloak, Auth0, etc) and emits user login events to downstream microservices.


## Key Features
* Handles login callbacks from any OIDC compliant Idp (eg, Keycloak, Auth0, etc)
* Exposes /me endpoint w standard claims info (user_id, roles, tenant_d, etc.)
* Emits user login events w standard claims info?


### Example flow
1. Frontend logs in via Keycloack/Auth0
2. Redirects to identity_gateway/login/callback
3. identity_gateway
   * Verifieds token
   * Extracts normalized claims
   * Emits event w standard identity claims
4. Any context (e.g Order) calls /me to get standard identity claims like
   ```json
   
   {
    "sub": "abc123",
    "email": "abc@email.com",
    "tenant_id": "tenant-abc",
     "roles": ["customer"]
    }
   

   ```

