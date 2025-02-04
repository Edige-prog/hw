from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from starlette import status
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


books_db = [
    {
        "id": 1,
        "title": "Atomic Habits",
        "author": "James Clear",
        "year": 2018,
        "total_pages": 320,
        "genre": "Self-help"
    },
    {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "year": 2008,
        "total_pages": 464,
        "genre": "Programming"
    },
]

# ID
def get_next_id():
    if not books_db:
        return 1
    return max(book["id"] for book in books_db) + 1



# create

@app.get("/books/new", response_class=HTMLResponse)
def get_new_book_form(request: Request):
    """
    GET /books/new
    Renders a form to create a new book.
    NOTE: This must be ABOVE /books/{book_id} to avoid route conflicts.
    """
    return templates.TemplateResponse("books/new.html", {"request": request})

@app.post("/books")
def create_book(
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    total_pages: int = Form(...),
    genre: str = Form(...)
):
    """
    POST /books
    Creates a new book in books_db.
    Then redirects to /books to display the updated list.
    """
    new_id = get_next_id()
    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "year": year,
        "total_pages": total_pages,
        "genre": genre
    }
    books_db.append(new_book)
    return RedirectResponse(url="/books", status_code=303)



# read


@app.get("/books", response_class=HTMLResponse)
def get_books(request: Request, page: int = 1):
    """
    GET /books
    Displays a list of books with pagination (10 items/page).
    Uses query param: ?page=1 by default
    """
    page_size = 10
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    paginated_books = books_db[start_index:end_index]

    total_books = len(books_db)
    last_page = (total_books + page_size - 1) // page_size 
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < last_page else None

    return templates.TemplateResponse(
        "books/list.html",
        {
            "request": request,
            "books": paginated_books,
            "current_page": page,
            "prev_page": prev_page,
            "next_page": next_page,
            "last_page": last_page
        }
    )

@app.get("/books/{book_id}", response_class=HTMLResponse)
def get_book_detail(request: Request, book_id: int):
    """
    GET /books/{book_id}
    Displays detail of a single book.
    If not found, returns "Not Found" with 404.
    """
    for book in books_db:
        if book["id"] == book_id:
            return templates.TemplateResponse(
                "books/detail.html",
                {"request": request, "book": book}
            )
    return PlainTextResponse("Not Found", status_code=404)

# delete and update

@app.get("/books/{book_id}/edit", response_class=HTMLResponse)
def edit_book_form(request: Request, book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return templates.TemplateResponse("books/edit.html", {"request": request, "book": book})
    return Response(content="Not Found", status_code=status.HTTP_404_NOT_FOUND)

@app.post("/books/{book_id}/edit")
def edit_book(book_id: int, title: str = Form(...), author: str = Form(...), year: int = Form(...), total_pages: int = Form(...), genre: str = Form(...)):
    for book in books_db:
        if book["id"] == book_id:
            book["title"] = title
            book["author"] = author
            book["year"] = year
            book["total_pages"] = total_pages
            book["genre"] = genre
            return RedirectResponse(url=f"/books/{book_id}", status_code=status.HTTP_303_SEE_OTHER)
    return Response(content="Not Found", status_code=status.HTTP_404_NOT_FOUND)

@app.post("/books/{book_id}/delete")
def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book["id"] == book_id:
            books_db.pop(i)
            return RedirectResponse(url="/books", status_code=status.HTTP_303_SEE_OTHER)
    return Response(content="Not Found", status_code=status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

