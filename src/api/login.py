from fastapi import APIRouter
from src import database as db
import sqlalchemy
from bcrypt import gensalt, hashpw
from pydantic import BaseModel

router = APIRouter()

# just checks yes or no if the user-passed in password matches 
# (not true perfect authorization)


def hash_and_salt_password(password):
    # Generate a random salt
    salt = gensalt()

    # Hash the password using the salt
    hashed_password = hashpw(password.encode('utf-8'), salt)

    # get the hashed and salted password
    return hashed_password.decode('utf-8')


class UserInfo(BaseModel):
    username: str
    password: str

@router.post("/login/", tags=["login"])
def add_user(userinfo: UserInfo):
    """
    This endpoint registers a new user, with a given username and password
    * `userinfo` is a class w/ two string attributes: username and password 

    Returns the id of the new user created 
    """

    with db.engine.connect() as conn:
        inserted_user = conn.execute(
            sqlalchemy.text(
            """
                INSERT INTO users (username, password)
                VALUES (:username, :password)
                RETURNING user_id;
            """
            ),
            {
                "username": userinfo.username,
                "password": hash_and_salt_password(userinfo.password)
            }
        )
        user = inserted_user.fetchone()
        conn.commit()
    return user.user_id
