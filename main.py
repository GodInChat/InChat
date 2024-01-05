import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis

from src.inchat.database.sql.postgres import database
from src.inchat.database.nosql.redis_cache import cache_database

from src.inchat.database.sql.models import User
from src.inchat.auth.service import current_user

from src.inchat.auth.routes import router as auth
from src.inchat.pdf.routes import router as pdf
from src.inchat.chat.routes import router as chat


app = FastAPI()

app.include_router(auth)
app.include_router(pdf)
app.include_router(chat)

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/example/healthchecker")
async def healthchecker(
    db: AsyncSession = Depends(database), cache: Redis = Depends(cache_database)
):
    print("postgres connection check...")
    await db.execute(text("SELECT 1"))
    print("redis connection check...")
    await cache.set("1", 1)
    return {"message": "Databases are OK!"}


@app.get("/example/user-authenticated")
async def authenticated_route(user: User = Depends(current_user)):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
    #  uvicorn main:app --host localhost --port 8000
