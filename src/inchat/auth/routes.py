from pathlib import Path

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from src.inchat.auth.schemas import UserRead, UserCreate, UserUpdate
from src.inchat.auth.service import auth_backend, fastapi_users, google_oauth_client, SECRET

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent / "templates")

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/user",
    tags=["user"],
)
