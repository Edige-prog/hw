from fastapi import APIRouter, Depends, HTTPException, Request, Form
from ..repo.flowers import FlowersRepository
from ..schemas.flowers import FlowerCreate, FlowerInfo
from fastapi.responses import RedirectResponse
router = APIRouter()


# GET /flowers - для показа списка цветов
# POST /flowers - добавление цветов
@router.get("/")
async def get_all_flowers():
    flowers = FlowersRepository.get_all_flowers()
    return flowers

@router.post("/")
async def create_flower(name: str = Form(...), quantity: int = Form(...), price: float = Form(...)):
    flower = FlowerCreate(name = name, price = price, quantity = quantity)
    FlowersRepository.create_flower(flower)
    RedirectResponse(url="/flowers", status_code=303)

@router.post("/{flower_id}", response_model=FlowerInfo)
async def get_flower_by_id(flower_id:int):
    flower = FlowersRepository.get_flower_by_id(flower_id)
    return flower


@router.delete("/{flower_id}")
async def delete_flower(flower_id:int):
    message = FlowersRepository.delete_flower_by_id(flower_id)
    return message