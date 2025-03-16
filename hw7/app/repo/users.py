from app.database.db import get_connection
from app.schemas.users import UserCreate, UserInfo, UserUpdate
from pydantic import EmailStr
from fastapi import HTTPException


class UserRepository:
    @classmethod
    def get_user_by_email(cls, email:EmailStr):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, email, full_name, password_hash, photo_url FROM users WHERE email=%s", (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return UserInfo(id=row[0], email=row[1], fullname=row[2], password_hashed=row[3], photo_url=row[4])

    @classmethod
    def get_user_by_id(cls, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, email, full_name, password_hash, photo_url FROM users WHERE id=%s", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return UserInfo(id=row[0], email=row[1], fullname=row[2], password_hashed=row[3], photo_url=row[4])


    @classmethod
    def create_user(cls, user_input:UserCreate):
        conn = get_connection()
        cur = conn.cursor()
        existing_user = cls.get_user_by_email(user_input.email)

        if existing_user:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        cur.execute("INSERT INTO users (email, full_name, password_hash) VALUES (%s, %s, %s)",
                    (user_input.email, user_input.fullname, user_input.password))
        conn.commit()
        cur.close()
        conn.close()
        new_user = cls.get_user_by_email(user_input.email)
        return new_user

    # @classmethod
    # def update_user(cls, user_id:int, user_input:UserUpdate):
    #     conn = get_connection()
    #     cur = conn.cursor()
    #     existing_user = cls.get_user_by_id(user_id)
    #
    #     if not existing_user:
    #         raise HTTPException(
    #             status_code=400, detail="User does not exist"
    #         )
    #
    #     cur.execute("")