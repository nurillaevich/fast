from fastapi import FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Car, Person

app = FastAPI()


async def get_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]}
)


@app.on_event("startup")
async def startup():
    await get_db()


Car_model = pydantic_model_creator(Car, name="Car")
Person_model = pydantic_model_creator(Person, name="Person")


@app.post("/cars")
async def create_car(car: Car_model):
    car = await Car.create(**car.dict())
    return car


@app.get("/cars")
async def get_cars():
    return await Car.all()


@app.put("/cars/{pk}")
async def update_car(pk: int, model: str, year: int, color: str):
    car = await Car.get_or_none(id=pk)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    car.model = model
    car.year = year
    car.color = color
    car.save()
    return car


@app.delete("/cars/{pk}")
async def delete_car(pk: int):
    car = await Car.get_or_none(id=pk)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await car.delete()
    return {"message": "Car deleted"}


@app.post("/persons")
async def create_person(person: Person_model):
    person = await Person.create(**person.dict())
    return person


@app.get("/persons")
async def get_persons():
    return await Person.all()


@app.put("/persons/{pk}")
async def update_person(pk: int, name: str, age: int, gender: str, image_url: str, car: str):
    person = await Person.get_or_none(id=pk)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    person.name = name
    person.age = age
    person.gender = gender
    person.image_url = image_url
    person.car = car
    person.save()
    return person


@app.delete("/persons/{pk}")
async def delete_person(pk: int):
    person = await Person.get_or_none(id=pk)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    person.delete()
    return {"message": "Person deleted"}
