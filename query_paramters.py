from enum import Enum
from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


# Query Parameters
# -------------------------

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

# http://127.0.0.1:8000/items/?skip=0&limit=10
# if they're parameters but not in the path then they are also url parameters. 
# These parameters are optional and default values will be used if not in the path
@app.get("/items2/")
async def read_item(skip: int=0, limit: int=10):
    return fake_items_db[skip : skip + limit]

# optional parameters that are otherwise none
# note that item_id is a path parameter and q is a query parameter
# FastAPI will know that q is optional because of the = None.
# The Optional in Optional[str] is not used by FastAPI (FastAPI will only use the str part), 
# but the Optional[str] will let your editor help you finding errors in your code.
from typing import Optional
@app.get("/items3/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Query Parameter Type Conversion
# --------------------------------------

# You can also declare bool types, and they will be converted
# the order of path and query parameters doesn't matter they're matched on name
@app.get("/items4/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that had a long description"}
        )
    return item

# When you declare a default value for non-path parameters (for now, we have only seen query parameters), then it is not required.
# If you don't want to add a specific value but just make it optional, set the default as None.
# But when you want to make a query parameter required, you can just not declare any default value:
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


