# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
# OAuth2 specifies that when using the "password flow" (that we are using) 
# the client/user must send a username and password fields as form data.
# for the login path operation, we need to use these names to be compatible with 
# the spec (and be able to, for example, use the integrated API documentation system).
# The spec also states that the username and password must be sent as form data (so, no JSON here).

# scope¶
# -----------------------------------------------------------------
# The spec also says that the client can send another form field "scope".
# The form field name is scope (in singular), but it is actually a long string with "scopes" separated by spaces.
# Each "scope" is just a string (without spaces).
# They are normally used to declare specific security permissions, for example:

#     users:read or users:write are common examples.
#     instagram_basic is used by Facebook / Instagram.
#     https://www.googleapis.com/auth/drive is used by Google.

# Info:
#   In OAuth2 a "scope" is just a string that declares a specific permission required.
#   It doesn't matter if it has other characters like : or if it is a URL.
#   Those details are implementation specific.
#   For OAuth2 they are just strings.


from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db ={
    "johndoe" : {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret1",
        "disabled": False
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True
    }
}

app = FastAPI()

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password:str

def get_user(db, username:str):

    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):

    # this doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


# The additional header WWW-Authenticate with value Bearer we are returning here is also part of the spec.
# Any HTTP (error) status code 401 "UNAUTHORIZED" is supposed to also return a WWW-Authenticate header.
# In the case of bearer tokens (our case), the value of that header should be Bearer.
# You can actually skip that extra header and it would still work.
# But it's provided here to be compliant with the specifications.
# Also, there might be tools that expect and use it (now or in the future) and that might be useful for you or your users, now or in the future.
async def get_current_user(token: str = Depends(oauth2_scheme)):

    user = fake_decode_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
    )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):

    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

# OAuth2PasswordRequestForm is a class dependency that declares a form body with:
# 
#     The username.
#     The password.
#     An optional scope field as a big string, composed of strings separated by spaces.
#     An optional grant_type.
# 
# The OAuth2 spec actually requires a field grant_type with a fixed value of password, but OAuth2PasswordRequestForm doesn't enforce it.
# 
# If you need to enforce it, use OAuth2PasswordRequestFormStrict instead of OAuth2PasswordRequestForm.
#     An optional client_id (we don't need it for our example).
#     An optional client_secret (we don't need it for our example).
# 
# Info
#   The OAuth2PasswordRequestForm is not a special class for FastAPI as is OAuth2PasswordBearer.
#   OAuth2PasswordBearer makes FastAPI know that it is a security scheme. So it is added that way to OpenAPI.
#   But OAuth2PasswordRequestForm is just a class dependency that you could have written yourself, or you could have declared Form parameters directly.
#   But as it's a common use case, it is provided by FastAPI directly, just to make it easier.

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm=Depends()):

    user_dict = fake_users_db.get(form_data.username)

    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # note ** serializes the dictionary to the Model class, names must match
    user = UserInDB(**user_dict)

    # "Hashing" means: converting some content (a password in this case) into a sequence of bytes (just a string) that looks like gibberish.
    # Whenever you pass exactly the same content (exactly the same password) you get exactly the same gibberish.
    # But you cannot convert from the gibberish back to the password.
    # Why use password hashing
    # If your database is stolen, the thief won't have your users' plaintext passwords, only the hashes.
    # So, the thief won't be able to try to use those same passwords in another system (as many users use the same password everywhere, this would be dangerous).
    hashed_password = fake_hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # The response of the token endpoint must be a JSON object.
    # It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".
    # And it should have an access_token, with a string containing our access token.
    # For this simple example, we are going to just be completely insecure and return the same username as the token.
    # This should be a jwt token
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

