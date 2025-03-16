from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.schemas.users import UserInfo, UserCreate, UserLogin, UserUpdate
from app.repo.users import UserRepository
from app.utils.security import hash_password, verify_password, create_jwt_token, decode_jwt_token
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/signup")
def get_signup_form(user_info:UserCreate):
    user_info.password = hash_password(user_info.password)
    new_user = UserRepository.create_user(user_info)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Successfully signed up.", "user_id": new_user.id}
    )


@router.post("/login")
def post_login(form_data: OAuth2PasswordRequestForm=Depends()):
    user = UserRepository.get_user_by_email(form_data.username)
    if not verify_password(form_data.password, user.password_hashed):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/{user_id}")
def post_login(user_id: int):
    user = UserRepository.get_user_by_id(user_id)
    return user


@router.patch("/me")
def patch_user(
        # user_input: UserUpdate,
        token: str = Depends(oauth2_scheme),
):
    user_id = decode_jwt_token(token)
    updated_user = UserRepository.get_user_by_id(user_id)
    return updated_user