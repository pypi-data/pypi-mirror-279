from sqlalchemy.orm import Session

from backend1.db import schemas


def create_user(db: Session, user: schemas.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def check_user(db:Session, user: schemas.User):
    result = db.query(schemas.User).filter(schemas.User.email == user.email, schemas.User.password == user.password).first()
    if result:
        return result.id
    else:
        return False