from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

cars = [
    {"name": "BMW", "year": 2020},
    {"name": "Audi", "year": 2021},
    {"name": "BMW X5", "year": 2022},
]


@app.get("/cars")
def get_cars(request: Request):
    return templates.TemplateResponse(
        "cars/search.html",
        {"request": request, "cars": cars}
    )


@app.get("/cars/search")
def search_cars(request: Request, car_name: str = ""):

    filtered_cars = [
        car for car in cars
        if car_name.lower() in car["name"].lower()
    ]

    return templates.TemplateResponse(
        "cars/search.html",
        {"request": request, "cars": filtered_cars}
    )


@app.get("/cars/new")
def new_car_form(request: Request):
    return templates.TemplateResponse(
        "cars/new.html",
        {"request": request}
    )


@app.post("/cars/new")
def create_car(name: str = Form(...), year: int = Form(...)):

    cars.append({
        "name": name,
        "year": year
    })

    return RedirectResponse("/cars", status_code=303)