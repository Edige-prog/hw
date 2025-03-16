from fastapi import APIRouter, Depends, HTTPException, Request, Form
from ..repo.flowers import FlowersRepository
from ..repo.users import UserRepository
from ..schemas.flowers import FlowerCreate, FlowerInfo
from fastapi.responses import RedirectResponse, HTMLResponse
from ..utils.security import oauth2_scheme, decode_jwt_token
router = APIRouter()


# GET /flowers - для показа списка цветов
# POST /flowers - добавление цветов
@router.get("/")
async def get_all_flowers(request: Request):
    token = request.cookies.get("access_token")
    user = None
    if token:
        user_id = decode_jwt_token(token)
        user = UserRepository.get_user_by_id(user_id)

    templates = request.app.state.templates
    return templates.TemplateResponse("flowers/flowers.html", {"request": request, "flowers": FlowersRepository.get_all_flowers(), "user": user})


@router.post("/")
async def create_flower(
    request: Request,
    name: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
):
    try:
        flower = FlowerCreate(
            name=name,
            quantity=quantity,
            price=price
        )
        FlowersRepository.create_flower(flower)
        return RedirectResponse(url="/flowers", status_code=303)
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{flower_id}", response_model=FlowerInfo)
async def get_flower_by_id(flower_id:int):
    flower = FlowersRepository.get_flower_by_id(flower_id)
    return flower


@router.delete("/{flower_id}")
async def delete_flower(flower_id:int):
    message = FlowersRepository.delete_flower_by_id(flower_id)
    return message