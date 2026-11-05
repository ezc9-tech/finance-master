from fastapi import FastAPI, Depends, HTTPException
import os
import requests
import base64
import bcrypt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.db.db import get_db
from backend.models.models import User
from backend.schema.schema import UserResponse, UserCreate


app = FastAPI()

@app.get("/net-worth")
def get_financial_data():
    try: 
        
        # 1. Get a Setup Token
        setup_token = os.getenv("SIMPLEFIN_TOKEN")

        # 2. Claim an Access URL
        claim_url = base64.b64decode(setup_token).decode('utf-8')
        response = requests.post(claim_url)
        access_url = response.text

        # 3. Get some data
        scheme, rest = access_url.split('//', 1)
        auth, rest = rest.split('@', 1)
        url = scheme + '//' + rest + '/accounts'
        username, password = auth.split(':', 1)
        
        response = requests.get(url, auth=(username, password), params={'version':'2'})
        data = response.json()
        
        accounts = data.get('accounts', [])
        net_worth = {}
        
        for account in accounts:
            currency = account["currency"]
            balance = account.get("balance", 0)
            if currency in net_worth:
                net_worth[currency] += balance
            else:
                net_worth[currency] = balance
        

        return {"response": net_worth}
    
    except Exception as e:
        return {"error": str(e)}


@app.post("/create-user", response_model=UserResponse)
def create_user(body: UserCreate, db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == body.email) | (User.username == body.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    hashed_password = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt())

    user = User(
        username=body.username,
        email=body.email,
        hashed_password=hashed_password.decode("utf-8"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user