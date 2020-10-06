from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

# Path Parameters
# -------------------------------------------------

# automatically validated and typed path parameters
@app.get("/items1/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# the order here matters
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# using enumerations to restrict values in and out
@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# In this case, the name of the parameter is file_path, and the last part,
#  :path, tells it that the parameter should match any path.
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


