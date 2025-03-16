from xmlrpc.client import ResponseError

from ..database.db import get_connection
from ..schemas.flowers import FlowerCreate, FlowerInfo
from fastapi import HTTPException


class FlowersRepository:
    @classmethod
    def create_flower(cls, flower:FlowerCreate):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO flowers (name, quantity, price)"
            "VALUES (%s, %s, %s)", (flower.name, flower.quantity, flower.price)
        )
        conn.commit()
        cur.close()
        conn.close()


    @classmethod
    def get_all_flowers(cls):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, name, quantity, price FROM flowers ORDER BY id DESC")
            rows = cur.fetchall()
            if rows is None:
                raise HTTPException(status_code=404, detail="Flower not found")
        finally:
            cur.close()
            conn.close()
        flowers = []
        for r in rows:
            flowers.append(FlowerInfo(id=r[0], name=r[1], quantity=r[2], price=r[3]))
        return flowers

    @classmethod
    def get_flower_by_id(cls, fid):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, name, quantity, price FROM flowers WHERE id=%s", (fid,))
            r = cur.fetchone()
            if r is None:
                raise HTTPException(status_code=404, detail="Flower not found")
        finally:
            cur.close()
            conn.close()
        if r:
            flower = FlowerInfo(id=r[0], name=r[1], quantity=r[2], price=r[3])
            return flower


    @classmethod
    def delete_flower_by_id(cls, fid):
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Check if the flower exists
            cur.execute("SELECT id FROM flowers WHERE id=%s", (fid,))
            r = cur.fetchone()
            if r is None:
                raise HTTPException(status_code=404, detail="Flower not found")

            # If found, proceed with deletion
            cur.execute("DELETE FROM flowers WHERE id=%s", (fid,))
            conn.commit()
        finally:
            cur.close()
            conn.close()

        return {"message": "Flower deleted successfully"}
