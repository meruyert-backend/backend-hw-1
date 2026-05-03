from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import engine, Base, SessionLocal
import models
from auth import hash_password
from auth import verify_password
from fastapi.responses import RedirectResponse
from auth import create_access_token
from dependencies import get_current_user
from fastapi import Depends

templates = Jinja2Templates(directory="templates")

app = FastAPI()

Base.metadata.create_all(bind=engine)

# GET/ signup ПОКАЗАТЬ ФОРМУ
@app.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {"request": request}
    )

# POST/ signup ОБРАБОТАТЬ И СОХРАНИТЬ
@app.post("/signup")
def signup(email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()

    user = models.User(
        email=email,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()

    return {"message": "User created"}


# GET/login ФОРМА ВХОДА
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# POST/login ПРОВЕРКА ПОЛЬЗОВАТЕЛЯ
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(password, user.password):
        return {"error": "Wrong password"}

    # 🔐 создаём токен
    token = create_access_token({"user_id": user.id})

    # 🍪 кладём в cookie
    response = RedirectResponse(url="/flowers", status_code=303)
    response.set_cookie(key="access_token", value=token)

    return response


@app.get("/flowers", response_class=HTMLResponse)
def flowers(request: Request, user = Depends(get_current_user)):
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request}
        )

    db = SessionLocal()
    flowers = db.query(models.Flower).all()

    return templates.TemplateResponse(
        "flowers.html",
        {"request": request, "flowers": flowers}
    )

@app.get("/add-test-flowers")
def add_test_flowers():
    db = SessionLocal()

    flower1 = models.Flower(name="Rose", price=10.5)
    flower2 = models.Flower(name="Tulip", price=7.0)
    flower3 = models.Flower(name="Lily", price=12.3)

    db.add_all([flower1, flower2, flower3])
    db.commit()

    return {"message": "Flowers added"}


@app.post("/add-to-cart/{flower_id}")
def add_to_cart(flower_id: int, user = Depends(get_current_user)):
    if not user:
        return {"error": "Not authenticated"}

    db = SessionLocal()

    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == user.id,
        models.CartItem.flower_id == flower_id
    ).first()

    if existing:
        existing.quantity += 1
    else:
        cart_item = models.CartItem(
            user_id=user.id,
            flower_id=flower_id,
            quantity=1
        )
        db.add(cart_item)
    db.commit()

    return RedirectResponse(url="/flowers", status_code=303)


@app.get("/cart", response_class=HTMLResponse)
def cart(request: Request, user = Depends(get_current_user)):
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request}
        )

    db = SessionLocal()

    cart_items = db.query(models.CartItem, models.Flower).join(
        models.Flower,
        models.CartItem.flower_id == models.Flower.id
    ).filter(
        models.CartItem.user_id == user.id
    ).all()

    total = sum(flower.price for _, flower in cart_items)

    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "cart_items": cart_items,
            "total": total
        }
    )

@app.post("/buy")
def buy(user = Depends(get_current_user)):
    if not user:
        return {"error": "Not authenticated"}

    db = SessionLocal()

    # 1. взять корзину пользователя
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == user.id
    ).all()

    # 2. создать заказы
    for item, flower in cart_items:
        order = models.Order(
            user_id=user.id,
            flower_id=item.flower_id
        )
        db.add(order)

    # 3. очистить корзину
    db.query(models.CartItem).filter(
        models.CartItem.user_id == user.id
    ).delete()

    db.commit()

    return RedirectResponse(url="/orders", status_code=303)


@app.get("/orders", response_class=HTMLResponse)
def orders(request: Request, user = Depends(get_current_user)):
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request}
        )

    db = SessionLocal()

    orders = db.query(models.Order, models.Flower).join(
        models.Flower,
        models.Order.flower_id == models.Flower.id
    ).filter(
        models.Order.user_id == user.id
    ).all()

    return templates.TemplateResponse(
        "orders.html",
        {"request": request, "orders": orders}
    )

@app.post("/remove-from-cart/{item_id}")
def remove_from_cart(item_id: int, user = Depends(get_current_user)):
    db = SessionLocal()

    db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user.id
    ).delete()

    db.commit()

    return RedirectResponse(url="/cart", status_code=303)