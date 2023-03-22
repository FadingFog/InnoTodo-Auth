from fastapi import APIRouter

from app.api.routers import auth, user

routes = APIRouter()

routes.include_router(user.router_registration)
routes.include_router(user.router)
routes.include_router(auth.router)
