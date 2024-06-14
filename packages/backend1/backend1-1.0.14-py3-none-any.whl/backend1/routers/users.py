from fastapi import APIRouter, Depends
from backend1.models.users import UserIn, UserLogin
from typing import Annotated
from backend1.operations.users import create_user, check_user
from backend1.db.database import SessionLocal
from backend1.db.schemas import User as UserSchema
from sqlalchemy.orm import Session
from backend1.auth.auth_handler import signJWT

router = APIRouter(
    prefix="/backend1/user",
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", tags=["users"])
async def signup_user(user: Annotated[UserIn, {"description": "User data to create"}], db: Annotated[Session,Depends(get_db)]):
    user_info:UserSchema = create_user(db, UserSchema(**user.model_dump()))
    return signJWT(user_info.id)

@router.post("/login", tags=["users"])
def user_login(userLogin: Annotated[UserLogin, {"description": "User data to create"}], db: Annotated[Session, Depends(get_db)]):
    user = UserSchema(**userLogin.model_dump())
    result = check_user(db, user)
    if result:
        return signJWT(result)
    return {
        "error": "Wrong login details!"
    }