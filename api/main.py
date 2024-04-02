import os
import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/info")
async def root():
    return "healthy"


# TODO: DELETE THIS ENDPOINT
@app.get("/env")
async def env():
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
