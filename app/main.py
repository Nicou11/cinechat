from fastapi import FastAPI
from app.chat_router import chat_router

app = FastAPI()

app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)