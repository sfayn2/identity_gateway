# identity_gateway
identity_gateway : A lightweight **Identity Gateway** that centrally handles login callback from  any selected IDPs (Keycloak, Auth0, etc) and emits user login events to downstream microservices.


## Key Features
* Handles login callbacks from any OIDC compliant Idp (eg, Keycloak, Auth0, etc)
* Exposes /me endpoint w standard claims info (user_id, roles, tenant_d, etc.)
* Emits user login events w standard claims info?


### Example flow
1. Frontend (https://ui.app2.com/login) redirect Keycloack/Auth0 to login (https://idp.app0.com)
2. Once Login, Redirects to identity_gateway/gateway/login_callback (https://idpgateway.app1.com)
3. identity_gateway
   * Exchanges code for tokens
   * Verifieds token
   * Extracts normalized claims
   * Emits event w standard identity claims
   * Set refresh token cookie
   * Redirect to frontend (https://ui.app2/com/ready)
4. Frontend (https://ui.app2.com/ready) immediately fetches access token via
```js
   await fetch("https://idpgateway/app1/refresh", {
      credentials: "include"
   })
```
5. Identity gateway replies with { access_token: "...", sub: "...", token_type: ".."}
6. Frontend stores access token in mem or localStorage?
5. Any context (e.g https://order.app3.com) calls /me to get standard identity claims like
   ```json
   
   {
    "sub": "abc123",
    "email": "abc@email.com",
    "tenant_id": "tenant-abc",
     "roles": ["customer"]
    }
   

   ```

