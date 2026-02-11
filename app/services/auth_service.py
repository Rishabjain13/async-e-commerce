from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_token,
)
from app.core.config import settings


class AuthService:
    def __init__(self, db):
        self.db = db

    # ---------------- REGISTER ---------------- #

    async def register(self, data):

        result = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(400, "Email already exists")

        user = User(
            email=data.email,
            password=hash_password(data.password),
            role="user",
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return {"message": "User registered successfully"}

    # ---------------- LOGIN ---------------- #

    async def login(self, data):

        result = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(401, "Invalid credentials")

        access_token = create_access_token(user.id, user.role)
        refresh_token = create_refresh_token(user.id, user.role)

        # 🔐 Store hashed refresh token in DB
        token_entry = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            is_revoked=False,
        )

        self.db.add(token_entry)
        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    # ---------------- REFRESH ---------------- #

    async def refresh(self, refresh_token: str):

        hashed = hash_token(refresh_token)

        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == hashed,
                RefreshToken.is_revoked == False,
            )
        )

        token_entry = result.scalar_one_or_none()

        if not token_entry:
            raise HTTPException(401, "Invalid refresh token")

        # 🔁 Rotate token (revoke old one)
        token_entry.is_revoked = True

        # Generate new tokens
        new_access = create_access_token(token_entry.user_id, "user")
        new_refresh = create_refresh_token(token_entry.user_id, "user")

        new_entry = RefreshToken(
            user_id=token_entry.user_id,
            token_hash=hash_token(new_refresh),
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            is_revoked=False,
        )

        self.db.add(new_entry)
        await self.db.commit()

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
        }

    # ---------------- LOGOUT ---------------- #

    async def logout(self, refresh_token: str):

        hashed = hash_token(refresh_token)

        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == hashed,
                RefreshToken.is_revoked == False,
            )
        )

        token_entry = result.scalar_one_or_none()

        if token_entry:
            token_entry.is_revoked = True
            await self.db.commit()

        return {"message": "Logged out successfully"}
