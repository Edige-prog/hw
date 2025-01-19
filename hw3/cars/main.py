from fastapi import FastAPI, Response, Request, Form
from fastapi.templating import Jinja2Templates
from cars import create_cars
import math
from starlette.responses import RedirectResponse

cars = create_cars(100)  # Здесь хранятся список машин
app = FastAPI()

templates = Jinja2Templates(directory="templates")

# (сюда писать решение)

@app.get("/")
def index():
    return Response("<a href='/cars'>Cars</a>")

# (сюда писать решение)

@app.get("/cars")
def pagination(request:Request, page:int = 1, limit:int = 10):
    return templates.TemplateResponse("cars.html", {"request":request, "cars":cars[(page-1)*limit:page*limit], "pages": {"total_pages":int(math.ceil(len(cars)/limit)), "current_page": page}, "limit":limit})

data_store = {}
@app.get("/cars/search")
def search(request:Request, page:int = 1, limit:int = 10, query:str=None):
    results = data_store.get('query')
    if query is None or query == "None":
        results = cars
    return templates.TemplateResponse("search.html", {"request":request, "cars":results[(page-1)*limit:page*limit], "pages": {"total_pages":int(math.ceil(len(results)/limit)), "current_page": page}, "limit":limit, "placeholder":query})

@app.post("/cars/search")
def results(query: str = Form(...)):
    results = []
    if query is not None:
        for car in cars:
            if query.lower() in car['name'].lower():
                results.append(car)
        data_store['query'] = results
    return RedirectResponse(f"/cars/search?query={query}", status_code=303)


@app.get("/cars/new")
def search(request:Request):
    return templates.TemplateResponse("new.html", {"request": request})

@app.post("/cars/new")
async def submit_comment(name: str = Form(...), year: str = Form(...)):
    cars.append({
        "id":len(cars)+1,
        "name":name,
        "year":year
    })
    return RedirectResponse(url="/cars", status_code=303)
