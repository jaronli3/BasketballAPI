from fastapi.testclient import TestClient
from fastapi import HTTPException

from src.api.server import app
from src.api.login import *
from src import database as db

client = TestClient(app)

def test_add_and_login_usera():
    reqbody = {
        "username": "username1234",
        "password": "password01"
    }   
    responsea = client.post("/adduser/", json=reqbody)
    assert responsea.status_code == 200

    responseb = client.post("/loginuser/", json=reqbody)
    assert responseb.status_code == 200
    assert responseb.json() == True 

def test_add_and_login_userb():
    reqbody = {
        "username": "asdf123",
        "password": "12345!!AB!"
    }   
    responsea = client.post("/adduser/", json=reqbody)
    assert responsea.status_code == 200

    badreqbody = {
        "username": "asdf123", 
        "password": "password11111"
    }

    responseb = client.post("/loginuser/", json=badreqbody)
    assert responseb.status_code == 200
    assert responseb.json() == False 
