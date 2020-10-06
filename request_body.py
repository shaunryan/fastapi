
# To declare a request body, you use Pydantic models with all their power and benefits.
# https://pydantic-docs.helpmanual.io/
# note to send a body request you should use one of POST, PUT, DELETE or PATCH
# Sending a body with a GET request has an undefined behavior in the specifications, 
# nevertheless, it is supported by FastAPI, only for very complex/extreme use cases.
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

# The same as when declaring query parameters, when a model attribute has a default value, 
# it is not required. Otherwise, it is required. Use None to make it just optional.
# e.g. both of these are valid:
# {
#     "name": "Foo",
#     "description": "An optional description",
#     "price": 45.2,
#     "tax": 3.5
# }
# {
#     "name": "Foo",
#     "price": 45.2
# }
# 
# With just that Python type declaration, FastAPI will:

#     Read the body of the request as JSON.
#     Convert the corresponding types (if needed).
#     Validate the data.
#         If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
#     Give you the received data in the parameter item.
#         As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for all of the attributes and their types.
#     Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
#     Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

@app.post("/items1/")
async def create_item(item: Item):
    return item

# pydantic gives us the benefit of having a typed request body.
@app.post("/items2/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Request body + path parameters
# -------------------------------------------------------------------------
# You can declare path parameters and body requests at the same time.
# FastAPI will recognize that the function parameters that match path parameters should be taken from the path, 
# and that function parameters that are declared to be Pydantic models should be taken from the request body.
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# Request body + path + query parameters
# -------------------------------------------------------------------------
# You can also declare body, path and query parameters, all at the same time.
# FastAPI will recognize each of them and take the data from the correct place.
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# The function parameters will be recognized as follows:

#     If the parameter is also declared in the path, it will be used as a path parameter.
#     If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
#     If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.

# FastAPI will know that the value of q is not required because of the default value = None.

# The Optional in Optional[str] is not used by FastAPI, but will allow your editor to give you better support and detect errors.