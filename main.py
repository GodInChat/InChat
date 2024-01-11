import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings

from src.inchat.database.sql.postgres import database

from src.inchat.database.sql.models import User
from src.inchat.auth.service import current_user

from src.inchat.auth.routes import router as auth
from src.inchat.pdf.routes import router as pdf
from src.inchat.chat.routes import router as chat


description = """
## Порядок дій

* **Створити свого цифрового двійника** (_Low-Rank Adaptation_, _заплановано_).
* **Завантажити свої роботи** Це не тільки PDF-файл оригінальної роботи, але також і допоміжні файли, що покращать відповіді цифрового двійника.
* **Взаємодія з користувачем** через будь який інтерфейс, наприклад, Телеграм бот @INCHAT_PRIME_BOT.
* **Зворотній зв'язок** з автором, якщо цифровий двійник виявив цікаві аспекти предметного діалогу з користувачем (_заплановано_)

## Routes

* **/pdf/uploads**: завантажити PDF-документ. Ім'я PDF-файлу має бути унікальним.
* **/chat/init**: створити новий чат. Треба зберігати chat id для того, щоб звертатися до нього.
* **/chat/new_message**: передати LLM-двійнику питання користувача стосовно певного попередньо завантаженого PDF-файла і отримати відповідь.
"""

app = FastAPI(
    title="✓InChat",
    description=description,
    summary="Чат-Аватар: твоя цифрова копія - ти твориш, вона доносить твої ідеї всім 🚀",
    version="3.2.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "GodInChat Team",
        "url": "https://github.com/GodInChat",
        "email": "GodInChat@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(auth)
app.include_router(pdf)
app.include_router(chat)


@app.get("/")
def read_root():
    return {"message": "InChat!"}


@app.get("/example/healthchecker")
async def healthchecker(
    db: AsyncSession = Depends(database)
):
    print("postgres connection check...")
    await db.execute(text("SELECT 1"))
    return {"message": "Databases are OK!"}


@app.get("/example/user-authenticated")
async def authenticated_route(user: User = Depends(current_user)):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
    #  uvicorn main:app --host localhost --port 8000
