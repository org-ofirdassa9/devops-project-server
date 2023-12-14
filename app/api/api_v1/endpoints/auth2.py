# import os
# from supabase import create_client, Client
# from fastapi import APIRouter, Depends, status, HTTPException
# import logging
# from app.schemas.login_request import LoginRequest
# from app.schemas.user_schema_supa import UserCreate
# from gotrue.errors import AuthApiError


# logger = logging.getLogger(__name__)
# router = APIRouter()
# url: str = "https://vvzagcgibstlvglrcrji.supabase.co"  # os.environ.get("SUPABASE_URL")
# key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ2emFnY2dpYnN0bHZnbHJjcmppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDIyMzc1NzEsImV4cCI6MjAxNzgxMzU3MX0.rDRob490wr6HQPs1Ae22SrRgPuhlIX8h4BC2SFN3TVs"  # os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(url, key)


# async def get_supabase_client():
#     return supabase


# def verify_user_auth(client: Client = Depends(get_supabase_client)):
#     # Check if the user is authenticated
#     user = client.auth.get_user()
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Couldn't get user"
#         )
#     return user


# @router.post("/sign_up")
# def sign_up(user_create: UserCreate):
#     try:
#         res = supabase.auth.sign_up({"email": user_create.email, "password": user_create.password})
#         logger.info("%s signed up, id: %s", user_create.email, res.user.id)
#         return res.user
#     except Exception as e:
#         return e.args
# #8fa11a2b-858b-4077-8fdb-30685bba998e

# @router.post("/sign_out")
# async def sign_out():
#     try:
#         res = await supabase.auth.sign_out()
#         return res
#     except Exception as e:
#         logger.error(e)


# @router.post("/sign_in")
# def sign_in(login_request: LoginRequest):
#     try:
#         res = supabase.auth.sign_in_with_password({"email": login_request.email, "password": login_request.password})
#         logger.info("%s signed in", res.user.email)
#         return res
#     except Exception as e:
#         logger.error("unsuccessful login for %s, %s", login_request.email, e)


# @router.get("/me")
# async def get_me(res: dict = Depends(verify_user_auth)):
#     return res.user.email


# @router.get("/{user_id}")
# async def get_me(user_id: int, res: dict = Depends(verify_user_auth)):
#     return user_id
