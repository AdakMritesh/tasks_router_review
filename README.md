FastAPI [Lambda] + PostgreSQL [Aurora] | Serverless infrastucture

Funciton URL to start a lambda instance.
https://spkgny3km2h45fkd56zoqp4zmm0kvpkf.lambda-url.eu-central-1.on.aws/

This is a public URL with no Auth configured and all CORS origins are allowed.
Please use sparingly.

App has some issues executing user create which underpins all other db operations.

**Update:**
- ~~Function URL no longer active.~~
- ~~The code seemingly fails while creating a sqlalchemy db session. The raw db session (psycopg2) however, seems fine.~~
- ~~Making some amends to the db connection flow.~~
- DB connection issues are resolved.
- Issue with user creation is being investigated.