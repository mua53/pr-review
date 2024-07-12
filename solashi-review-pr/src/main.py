from fastapi import FastAPI
from git_providers.router import router 


app = FastAPI()

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}