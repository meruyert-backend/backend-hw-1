from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


books = [
    {
        "id": i,
        "title": f"Book {i}",
        "author": f"Author {i}",
        "year": 2000 + i,
        "total_pages": 100 + i,
        "genre": "Fiction"
    }
    for i in range(1, 51)
]


# GET /books (список + пагинация)
@app.get("/books")
def get_books(request: Request, page: int = 1):
    per_page = 10

    start = (page - 1) * per_page
    end = start + per_page

    paginated_books = books[start:end]

    has_next = end < len(books)
    has_prev = page > 1

    return templates.TemplateResponse(
        "books/list.html",
        {
            "request": request,
            "books": paginated_books,
            "page": page,
            "has_next": has_next,
            "has_prev": has_prev
        }
    )

# 🔹 GET /books/new (форма)
@app.get("/books/new")
def new_book(request: Request):
    return templates.TemplateResponse(
        "books/new.html",
        {"request": request}
    )

# 🔹 GET /books/{id} (детали книги)
@app.get("/books/{book_id}")
def get_book_detail(request: Request, book_id: int):
    for book in books:
        if book["id"] == book_id:
            return templates.TemplateResponse(
                "books/detail.html",
                {
                    "request": request,
                    "book": book
                }
            )

    raise HTTPException(status_code=404, detail="Not Found")



# POST /books (создание книги)
@app.post("/books")
def create_book(
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    total_pages: int = Form(...),
    genre: str = Form(...)
):
    new_id = len(books) + 1

    book = {
        "id": new_id,
        "title": title,
        "author": author,
        "year": year,
        "total_pages": total_pages,
        "genre": genre
    }

    books.append(book)

    return RedirectResponse(url="/books", status_code=303)