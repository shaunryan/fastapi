# https://fastapi.tiangolo.com/tutorial/security/get-current-user/
from typing import Optional
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", 
        email="shaun_chiburi@hotmail.com",
        full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

# Notice that we declare the type of current_user as the Pydantic model User.
# This will help us inside of the function with all the completion and type checks.
# You might remember that request bodies are also declared with Pydantic models.
# Here FastAPI won't get confused because you are using Depends.
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user))
    return current_user



