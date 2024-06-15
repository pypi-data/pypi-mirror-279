from pydantic import BaseModel, EmailStr

class User(BaseModel):
    fullname: str
    email: EmailStr
    
class UserIn(User):
    password: str

    class Config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True