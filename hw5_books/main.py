from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# "База данных"
books = [
    {"id": 1, "title": "Harry Potter", "author": "Rowling"},
    {"id": 2, "title": "1984", "author": "Orwell"},
]

# Найти книгу
def get_book_by_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


# СПИСОК КНИГ
@app.get("/books", response_class=HTMLResponse)
def list_books(request: Request):
    return templates.TemplateResponse(
        "books/list.html",
        {"request": request, "books": books}
    )


# СОЗДАНИЕ ФОРМА
@app.get("/books/new")
def new_book_form(request: Request):
    return templates.TemplateResponse(
        "books/new.html",
        {"request": request}
    )


# СОЗДАНИЕ КНИГИ
@app.post("/books")
def create_book(title: str = Form(...), author: str = Form(...)):
    new_id = max([b["id"] for b in books]) + 1 if books else 1

    book = {"id": new_id, "title": title, "author": author}
    books.append(book)

    return RedirectResponse(url="/books", status_code=303)


# ПОКАЗ КНИГИ
@app.get("/books/{id}")
def show_book(request: Request, id: int):
    book = get_book_by_id(id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return templates.TemplateResponse(
        "books/show.html",
        {"request": request, "book": book}
    )


# EDIT FORM
@app.get("/books/{id}/edit")
def edit_book_form(request: Request, id: int):
    book = get_book_by_id(id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return templates.TemplateResponse(
        "books/edit.html",
        {"request": request, "book": book}
    )


# UPDATE
@app.post("/books/{id}/edit")
def update_book(
    id: int,
    title: str = Form(...),
    author: str = Form(...)
):
    book = get_book_by_id(id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book["title"] = title
    book["author"] = author

    return RedirectResponse(url=f"/books/{id}", status_code=303)


# DELETE
@app.post("/books/{id}/delete")
def delete_book(id: int):
    book = get_book_by_id(id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    books.remove(book)

    return RedirectResponse(url="/books", status_code=303)