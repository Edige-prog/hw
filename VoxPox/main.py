from fastapi import FastAPI, Request, Response, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import RedirectResponse
import datetime
import math
app = FastAPI()


comments = []

templates = Jinja2Templates(directory="templates")

class Comment(BaseModel):
    comment_type: str
    comment_text: str
    timestamp: datetime

    class Config:
        arbitrary_types_allowed = True  # Allow datetime type

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'timestamp'):
            self.timestamp = datetime.datetime.now()

for i in range(10):
    comments.append(Comment(comment_type="Positive", comment_text=f"{i} - comment", timestamp = datetime.datetime.now()))


@app.get("/")
async def feed(request: Request, page:int = 1, limit:int = 3):
    start = -1-(page-1)*limit
    end = -1 - page*limit
    return templates.TemplateResponse("feed.html", {"request": request, "comments":comments[start:end:-1],"pages": {"total_pages":int(math.ceil(len(comments)/limit)), "current_page": page}, "limit":limit})


@app.get('/comment')
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/comment/post")
async def submit_comment(comment_type: str = Form(...), comment_text: str = Form(...)):
    # Validate the type of comment
    if comment_type not in ["positive", "negative"]:
        return {"error": "Invalid comment type"}

    new = Comment(comment_type=comment_type, comment_text=comment_text, timestamp=datetime.datetime.now())
    comments.append(new)
    # Process the comment (e.g., save it to  a database, print it, etc.)
    # For demonstration, we'll just return the comment data
    return RedirectResponse(url="/", status_code=303)
