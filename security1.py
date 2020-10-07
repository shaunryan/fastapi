# https://fastapi.tiangolo.com/tutorial/security/

# pip install python-multipart
# This is because OAuth2 uses "form data" for sending the username and password.

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# here tokenUrl="token" refers to a relative URL token that we haven't created yet. As it's a relative URL, it's equivalent to ./token.
# Because we are using a relative URL, if your API was located at https://example.com/, then it would refer to https://example.com/token. But if your API was located at https://example.com/api/v1/, then it would refer to https://example.com/api/v1/token.
# Using a relative URL is important to make sure your application keeps working even in an advanced use case like
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Go to the interactive docs at: http://127.0.0.1:8000/docs
# note the authorization button
@app.get("/items/")
# This parameter doesn't create that endpoint / path operation, 
# but declares that the URL /token will be the one that the client should use to get the token. 
# That information is used in OpenAPI, and then in the interactive API documentation systems.
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

