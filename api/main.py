import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/v1/info")
async def root():
    return "healthy"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
