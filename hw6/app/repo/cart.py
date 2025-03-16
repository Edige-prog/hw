from fileinput import close
from fastapi import HTTPException, Request
from ..database.db import get_connection
from ..repo.flowers import FlowersRepository
from ..schemas.cart import PurchaseItemInfo

from fastapi import Depends

from ..schemas.flowers import FlowerInfo


class CartRepository:
    @classmethod
    def add_purchase(cls, uid):
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Insert and return the newly created ID
            cur.execute("INSERT INTO purchase (user_id) VALUES (%s) RETURNING id", (uid,))
            purchase_id = cur.fetchone()[0]  # Fetch the new purchase ID
            conn.commit()
        finally:
            cur.close()
            conn.close()

        return purchase_id  # Return the newly created purchase ID


    @classmethod
    def add_purchase_item(cls, pid, fid, quantity):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO purchase_item (purchase_id, flower_id, quantity) VALUES (%s, %s, %s)", (pid, fid, quantity))
        conn.commit()
        cur.close()
        conn.close()


    @classmethod
    def get_purchases(cls, uid):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, user_id FROM purchase WHERE user_id=%s",
            (uid,))
        purchases = cur.fetchall()
        if not purchases:  # Check if the list is empty
            raise HTTPException(status_code=404, detail="Purchases not found")

        result = []
        for purchase in purchases:
            cur.execute(
                "SELECT id, flower_id, quantity FROM purchase_item WHERE purchase_id=%s",
                (purchase[0],)  # Use purchase[0] instead of undefined row[0]
            )
            purchase_items = cur.fetchall()
            items = []
            for purchase_item in purchase_items:
                flower = FlowersRepository.get_flower_by_id(purchase_item[1])
                items.append(PurchaseItemInfo(id=purchase_item[0], flower = flower, quantity=purchase_item[2]))
            result.append({"purchase_id": purchase[0], "purchase_items": items})

        cur.close()
        conn.close()
        return result


    @classmethod
    def get_cart(cls, request:Request):
        val = request.cookies.get("cart")
        if not val:
            return None

        flowers = []
        rows = val.split(';')
        for row in rows:
            if row != '':
                items = row.split(',')
                flower = FlowersRepository.get_flower_by_id(items[0])
                quantity = int(items[1])
                flowers.append({'flower':flower, 'quantity':quantity})

        return flowers
