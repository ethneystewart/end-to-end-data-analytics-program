from fastapi import FastAPI
from pydantic import BaseModel

# builds a application object - defines behaviour
app = FastAPI()

#memory
numbers = []
items = []
next_id = 1

#defines what a request body must look like 
class NumberInput(BaseModel):
    number: int # expect json , must contain a field called number and the type myust be int

class ItemCreate(BaseModel):
    name: str
    price: float


@app.get("/hello") # when get request comes to /hello run function below Routes
def say_hello():
    return {"message": "hello"}

@app.post("/add-number")
def add_number(input: NumberInput): # gets request body and validate it using class 
    numbers.append(input.number)
    return {
        "numbers": numbers,
        "count": len(numbers)
    }


@app.get("/items")
def get_items():
    return {"items": items.copy()}


@app.post("/items", status_code=201)
def create_item(payload: ItemCreate):
    global next_id # need to attach global because this is 

    new_item = {
        "id": next_id,
        "name": payload.name,
        "price": payload.price,
    }
    next_id += 1
    items.append(new_item)
    return new_item