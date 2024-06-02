import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token


def get_google_redirect_uri():
    return "https://ragapp-hw2k5v4d7q-uc.a.run.app"


auth_scheme = OAuth2AuthorizationCodeBearer(
    f"https://accounts.google.com/o/oauth2/auth?response_type=code&"
    f"client_id={os.environ['GOOGLE_CLIENT_ID']}&"
    f"redirect_uri={get_google_redirect_uri()}&"
    f"scope=openid%20profile%20email&access_type=offline",
    os.environ["TOKEN_URL"],
)


async def verify_token(token: str = Depends(auth_scheme)):
    try:
        id_info = id_token.verify_oauth2_token(
            token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )
        return {"message": "Access granted", "user_info": id_info}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
