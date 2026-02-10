from fastapi import APIRouter, Depends
from app.database.session import get_db
from app.schemas.address import AddressCreate
from app.controllers.address_controller import (
    create_address,
    get_user_addresses
)

router = APIRouter(prefix="/addresses", tags=["Addresses"])

USER_ID = 1


@router.post("/")
async def add_address(payload: AddressCreate, db=Depends(get_db)):
    return await create_address(db, USER_ID, payload)


@router.get("/")
async def list_addresses(db=Depends(get_db)):
    return await get_user_addresses(db, USER_ID)
