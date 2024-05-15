import os

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from rag_service import RagService
from security import verify_credential

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

app = FastAPI()


@app.get("/info")
async def root():
    return "healthy"


rag_service = RagService()
auth_scheme = HTTPBearer()


# TODO: DELETE THIS ENDPOINT
@app.get("/env")
async def env(credentials=Depends(auth_scheme)):
    verify_credential(credentials.credentials)
    return {
        "DATABASE_IP": os.environ["DATABASE_IP"],
        "DATABASE_USER": os.environ["DATABASE_USER"],
        "DATABASE_PASSWORD": os.environ["DATABASE_PASSWORD"],
        "PROJECT_ID": os.environ["PROJECT_ID"],
        "VECTOR_INDEX_REGION": os.environ["VECTOR_INDEX_REGION"],
        "VECTOR_INDEX_BUCKET": os.environ["VECTOR_INDEX_BUCKET"],
        "VECTOR_INDEX_ID": os.environ["VECTOR_INDEX_ID"],
        "ENDPOINT_ID": os.environ["ENDPOINT_ID"],
    }


@app.get("/response")
async def get_response(prompt: str, credentials=Depends(auth_scheme)):
    verify_credential(credentials.credentials)
    return {"response": rag_service.get_response(prompt)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
