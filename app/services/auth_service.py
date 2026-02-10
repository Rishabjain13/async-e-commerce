from sqlalchemy.future import select
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from fastapi import HTTPException


class AuthService:
    def __init__(self, db):
        self.db = db

    async def register(self, data):
        result = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        if result.scalar():
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(
            email=data.email,
            password=hash_password(data.password),
            role="user"
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return {"message": "User registered successfully"}

    async def login(self, data):
        result = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar()

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access = create_access_token(user.id, user.role)
        refresh = create_refresh_token(user.id, user.role)

        return {
            "access_token": access,
            "refresh_token": refresh
        }
