from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from app.schemas.users import UserInfo, UserCreate, UserLogin, UserUpdate
from app.repo.users import UserRepository
from app.utils.security import hash_password, verify_password, create_jwt_token, decode_jwt_token, oauth2_scheme
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pathlib import Path


# templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
router = APIRouter()


@router.get("/signup", response_class=HTMLResponse)
def get_signup_form(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("auth/sign-up.html", {"request": request})


@router.post("/signup")
def get_signup_form(user_info:UserCreate):
    user_info.password = hash_password(user_info.password)
    new_user = UserRepository.create_user(user_info)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Successfully signed up.", "user_id": new_user.id}
    )

@router.get("/login", response_class=HTMLResponse)
def get_signup_form(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
def post_login(email: str = Form(...), password: str = Form(...)):
    user = UserRepository.get_user_by_email(email)
    if not verify_password(password, user.password_hashed):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt_token(user.id)
    
    # Create redirect response
    response = RedirectResponse(url="/flowers", status_code=status.HTTP_303_SEE_OTHER)
    
    # Set both the Authorization header and cookie
    response.headers["Authorization"] = f"Bearer {access_token}"
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Makes the cookie inaccessible to JavaScript
        secure=True,    # Only send over HTTPS
        samesite="lax"  # Provides some CSRF protection
    )
    
    return response


@router.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    response = RedirectResponse(
        url="/auth/login",
        status_code=status.HTTP_303_SEE_OTHER
    )
    
    # Clear the access token cookie by setting it to empty and making it expire
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    # Clear Authorization header
    response.headers["Authorization"] = ""
    
    return response


# @router.post("/login")
# def post_login(form_data: OAuth2PasswordRequestForm=Depends()):
#     user = UserRepository.get_user_by_email(form_data.username)
#     if not verify_password(form_data.password, user.password_hashed):
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token = create_jwt_token(user.id)
#
#     # Create redirect response
#     response = RedirectResponse(url="/flowers", status_code=status.HTTP_303_SEE_OTHER)
#
#     # Set Authorization header with Bearer token
#     response.headers["Authorization"] = f"Bearer {access_token}"
#
#     # Also set token as a cookie for backup (some browsers might strip Authorization header on redirect)
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         secure=True,
#         samesite="lax"
#     )
#
#     return response


# @router.get("/{user_id}")
# def get_user_by_id(user_id: int):
#     user = UserRepository.get_user_by_id(user_id)
#     return user


@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        user_id = decode_jwt_token(token)
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return RedirectResponse(
                url="/auth/login",
                status_code=status.HTTP_303_SEE_OTHER
            )
        
        templates = request.app.state.templates
        return templates.TemplateResponse("auth/profile.html", {
            "request": request,
            "user": user
        })
    except HTTPException as he:
        # Handle authentication errors by redirecting to login
        return RedirectResponse(
            url="/auth/login",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        # Handle any other unexpected errors)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )