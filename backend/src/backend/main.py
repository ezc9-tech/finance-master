from fastapi import FastAPI
import os
import requests
import base64
from backend.routes.authRoutes import auth_router


app = FastAPI()

app.include_router(auth_router)

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
        response.status_code = 500
        return {"error": str(e)}
