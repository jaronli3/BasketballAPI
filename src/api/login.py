from fastapi import APIRouter
from src import database as db
import sqlalchemy
from bcrypt import gensalt, hashpw, checkpw
from pydantic import BaseModel

router = APIRouter()

class UserInfo(BaseModel):
    username: str
    password: str

def hash_and_salt_password(password):
    # Generate a random salt
    salt = gensalt()

    # Hash the password using the salt
    hashed_password = hashpw(password.encode('utf-8'), salt)

    # get the hashed and salted password
    return hashed_password.decode('utf-8')

def check_password(entered_password, hashed_password):
    return checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))


@router.post("/adduser/", tags=["login"])
def add_user(userinfo: UserInfo):
    """
    This endpoint registers a new user, with a given username and password
    * `userinfo` is a class w/ two string attributes: username and password 

    Returns the id of the new user created 
    """

    with db.engine.begin() as conn:
        inserted_user = conn.execute(
            sqlalchemy.text(
            """
                INSERT INTO users (username, hashed_password)
                VALUES (:username, :password)
                RETURNING user_id;
            """
            ),
            {
                "username": userinfo.username,
                "password": hash_and_salt_password(userinfo.password)
            }
        )
        user = inserted_user.scalar_one()
    return user

@router.post("/loginuser/", tags=["login"])
def user_login(userinfo: UserInfo):
    """
    This endpoint checks that a user's entered username and password 
    match what is stored in the database
    (just checks yes or no if the user-passed in password matches 
    (not true perfect authorization))
    * `userinfo` is a class w/ two string attributes: username and password 

    Returns a string for if the user login was successful 
    """

    with db.engine.begin() as conn:
        hashed_password = conn.execute(
            sqlalchemy.text(
            """
                SELECT hashed_password
                FROM users
                WHERE username = :username
            """
            ), {"username": userinfo.username}
        ).scalar_one()
    # check the password matches 
    return check_password(userinfo.password, hashed_password)

