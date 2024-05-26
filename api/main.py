from datetime import datetime
import os
from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import sqlalchemy as sql
from contextlib import asynccontextmanager
import time

from rag_service import RagService
from models import ClientMessage, RagMessage
from database import database, user_history
from security import verify_token


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


@asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield

    await database.disconnect()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",  # Frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/info")
async def root():
    return "healthy"


rag_service = RagService()


# TODO: DELETE THIS ENDPOINT
@app.get("/env")
async def env(credentials=Security(verify_token)):
    return {
        "DATABASE_IP": os.environ["DATABASE_IP"],
        "DATABASE_USER": os.environ["DATABASE_USER"],
        "DATABASE_PASSWORD": os.environ["DATABASE_PASSWORD"],
        "PROJECT_ID": os.environ["PROJECT_ID"],
        "VECTOR_INDEX_REGION": os.environ["VECTOR_INDEX_REGION"],
        "VECTOR_INDEX_BUCKET": os.environ["VECTOR_INDEX_BUCKET"],
        "VECTOR_INDEX_ID": os.environ["VECTOR_INDEX_ID"],
        "ENDPOINT_ID": os.environ["ENDPOINT_ID"],
        "GOOGLE_CLIENT_ID": os.environ["GOOGLE_CLIENT_ID"],
        "GOOGLE_CLIENT_SECRET": os.environ["GOOGLE_CLIENT_SECRET"],
        "GOOGLE_REDIRECT_URI": os.environ["GOOGLE_REDIRECT_URI"]
    }


@app.get("/user-info")
async def get_user_info(credentials=Security(verify_token)):
    return credentials


# chatbot endpoints
@app.post("/chatbot/message/new")
async def get_response(message: ClientMessage, credentials=Security(verify_token)):
    start = time.time_ns()
    query = user_history.insert().values(username=credentials["user_info"]["email"], prompt=message.text)
    await database.execute(query)
    response_time = time.time_ns() - start
    response = RagMessage(text=(await rag_service.get_response(message.text)), response_time=response_time)
    select_query = (
        user_history
        .select()
        .where(user_history.c.username == credentials["user_info"]["email"])
        .order_by(sql.desc(user_history.c.id))
        .limit(1)
    )

    record = await database.fetch_one(select_query)

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    update_query = (
        user_history.update()
        .where(user_history.c.id == record["id"])
        .values(
            response=response.text,
            response_time=response.response_time
        )
    )

    await database.execute(update_query)
    return response


@app.delete("/chatbot/message/{message_id}/delete")
async def delete_message(message_id, credentials=Security(verify_token)):
    query = user_history.select().where(user_history.c.id == int(message_id))
    record = await database.fetch_one(query)

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    # Delete the record
    delete_query = user_history.delete().where(user_history.c.id == int(message_id))
    await database.execute(delete_query)

    return {"message": "Record deleted successfully"}


@app.get("/chatbot/message/fetchAll")
async def get_all_messages(credentials=Security(verify_token)):
    query = (
        user_history.select()
        .where(user_history.c.username == credentials["user_info"]["email"])
    )

    results = await database.fetch_all(query)

    if not results:
        raise HTTPException(status_code=404, detail="No records found")

    return results


# auth endpoints
@app.get("/login")
async def login():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={os.environ['GOOGLE_CLIENT_ID']}&redirect_uri={os.environ['GOOGLE_REDIRECT_URI']}&scope=openid%20profile%20email&access_type=offline"
    }


@app.get("/auth")
async def auth(code):
    token_url = os.environ["TOKEN_URL"]
    data = {
        "code": code,
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": os.environ["GOOGLE_REDIRECT_URI"],
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_json = response.json()

    if 'error' in token_json:
        raise HTTPException(status_code=400, detail=f"Error in token request: {token_json['error']}")

    id_info = id_token.verify_oauth2_token(token_json['id_token'], google_requests.Request(), os.environ["GOOGLE_CLIENT_ID"])
    return {"id_info": id_info, "token_json": token_json}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
