from fastapi import HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
import json


with open("credentials/env_vars.json", "r") as f:
    env_vars = json.load(f)
for rec in env_vars:
    os.environ[rec["name"]] = rec["value"]

auth_scheme = OAuth2AuthorizationCodeBearer(f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={os.environ['GOOGLE_CLIENT_ID']}&redirect_uri={os.environ['GOOGLE_REDIRECT_URI']}&scope=openid%20profile%20email&access_type=offline", os.environ["TOKEN_URL"])


async def verify_token(token: str = Depends(auth_scheme)):
    try:
        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))
        return {"message": "Access granted", "user_info": id_info}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
