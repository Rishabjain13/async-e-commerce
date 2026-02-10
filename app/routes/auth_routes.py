from fastapi import APIRouter, Depends
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService
from app.database.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(data: RegisterRequest, db=Depends(get_db)):
    service = AuthService(db)
    return await service.register(data)


@router.post("/login")
async def login(data: LoginRequest, db=Depends(get_db)):
    service = AuthService(db)
    return await service.login(data)
