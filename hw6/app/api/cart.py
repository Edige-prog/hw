from urllib import request

from fastapi import APIRouter, Depends, HTTPException, Request, Form

from ..repo.cart import CartRepository
from ..repo.flowers import FlowersRepository
from ..schemas.flowers import FlowerCreate, FlowerInfo
import uuid
from fastapi.responses import RedirectResponse, JSONResponse
from ..utils.security import decode_jwt_token, oauth2_scheme
from ..database.db import get_connection
from ..repo.users import UserRepository


router = APIRouter()

@router.get("/")
async def get_cart_items(request: Request):
    token = request.cookies.get("access_token")
    user = None
    if token:
        user_id = decode_jwt_token(token)
        user = UserRepository.get_user_by_id(user_id)

    cart = CartRepository.get_cart(request)
    templates = request.app.state.templates
    totalsum = 0
    if cart:
        for item in cart:
            totalsum += item['flower'].price*item['quantity']
    return templates.TemplateResponse("cart/cart.html", {"request": request, "cart": cart, 'totalsum': totalsum, "user": user})


@router.post("/")
def post_cart_items(request: Request, flower_id: int = Form(...)):
    flower = FlowersRepository.get_flower_by_id(flower_id)

    cart = CartRepository.get_cart(request)
    cookie_val = ""
    new = True
    if cart:
        for row in cart:
            if row['flower'].id == flower_id:
                cookie_val += f'{row["flower"].id},{row["quantity"]+1};'
                new = False
            else:
                cookie_val += f'{row["flower"].id},{row["quantity"]};'

    if new:
        cookie_val += f'{flower_id},1'

    r = RedirectResponse(url="/cart", status_code=303)
    r.set_cookie(key="cart", value=cookie_val, httponly=True)
    return r


# @router.delete("/{flower_id}")
# async def delete_from_cart(
#     request: Request,
#     flower_id: int,
#     # token: str = Depends(oauth2_scheme)
# ):
#     response = RedirectResponse(url="/cart", status_code=303)
#     cart = request.cookies.get("cart", "")
#
#     if not cart:
#         return response
#
#     # Split the cart string into items
#     items = [item for item in cart.split(";") if item]
#
#     # Find and remove the item with the specified flower_id
#     new_items = []
#     for item in items:
#         if item:
#             current_id, quantity = item.split(",")
#             if int(current_id) != flower_id:
#                 new_items.append(item)
#
#     # Join the remaining items back into a string
#     new_cart = ";".join(new_items)
#
#     # Set the new cookie
#     response.set_cookie(key="cart", value=new_cart, httponly=True)
#
#     return response

@router.delete("/")
def delete_cart_item(request: Request, flower_id:int):
    flower = FlowersRepository.get_flower_by_id(flower_id)

    cart = CartRepository.get_cart(request)
    cookie_val = ""
    new = True

    for row in cart:
        if row['flower'].id == flower_id:
            if row['quantity'] > 1:
                cookie_val += f'{row["flower"].id},{row["quantity"]-1};'
            new = False
        else:
            cookie_val += f'{row["flower"].id},{row["quantity"]};'

    if new:
        raise HTTPException(status_code=404, detail="Your cart does not contain this flower")

    r = RedirectResponse(url="/cart", status_code=303)
    r.set_cookie(key="cart", value=cookie_val, httponly=True)
    return r


@router.get("/purchased")
def get_purchase(
        request: Request,
        token: str = Depends(oauth2_scheme),
):
    uid = decode_jwt_token(token)
    purchases = CartRepository.get_purchases(uid)

    user = UserRepository.get_user_by_id(uid)
    templates = request.app.state.templates

    total_items = 0
    total_spend = 0
    spends = {}
    for purchase in purchases:
        purchase_spend = 0
        for items in purchase['purchase_items']:

            total_items += items.quantity
            purchase_spend += items.flower.price*items.quantity

        spends[purchase['purchase_id']] = purchase_spend
        print(spends[purchase['purchase_id']])
        total_spend += purchase_spend

    return templates.TemplateResponse("cart/purchase.html", {"request": request, "user": user, "purchases": purchases, "total_items": total_items, "total_purchases": len(purchases), "total_spend": total_spend, "spends":spends})



@router.post("/purchased")
def post_purchase(
    request: Request,  # Add request parameter
    token: str = Depends(oauth2_scheme),
):
    cart = CartRepository.get_cart(request)

    # Check quantities before making any changes
    for row in cart:
        if row['flower'].quantity < row['quantity']:
            raise HTTPException(
                status_code=400, 
                detail=f"You're trying to buy {row['quantity']} of {row['flower'].name} flowers. But only {row['flower'].quantity} available."
            )

    user_id = decode_jwt_token(token)
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Start transaction
        cur.execute("BEGIN")
        
        # Create purchase
        new_purchase_id = CartRepository.add_purchase(user_id)
        
        # Add items and update flower quantities
        for row in cart:
            CartRepository.add_purchase_item(new_purchase_id, row['flower'].id, row['quantity'])
            
            # Update flower quantity
            cur.execute(
                "UPDATE flowers SET quantity = quantity - %s WHERE id = %s",
                (row['quantity'], row['flower'].id)
            )
        
        # Commit transaction
        cur.execute("COMMIT")

        response = RedirectResponse(url="/cart/purchased", status_code=303)

        response.delete_cookie("cart")
        
        # Clear the cart by setting an expired cookie
        return response
        
    except Exception as e:
        # Rollback in case of error
        cur.execute("ROLLBACK")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


