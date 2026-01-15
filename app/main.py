from flask import Flask, jsonify
from tortoise import Tortoise
from database.models.user import Users
import asyncio
import atexit

app = Flask(__name__, template_folder="templates", static_folder="static")

def run_async(coro):
    """Запуск асинхронной функции"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

async def init_db():
    """Инициализация БД"""
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["database.models.user"]}
    )
    await Tortoise.generate_schemas()
    print("✅ БД инициализирована")

async def close_db():
    """Закрытие соединений"""
    await Tortoise.close_connections()
    print("✅ Соединения с БД закрыты")

def cleanup():
    """Функция очистки при выходе"""
    print("🔄 Закрываю соединения с БД...")
    run_async(close_db())

# Инициализируем БД при запуске
run_async(init_db())

# Регистрируем очистку при выходе
atexit.register(cleanup)

@app.route("/")
def home():
    user = run_async(Users.create(username="Muhkhamed", balance=700))
    return jsonify({"id": user.id, "name": user.username, "balance": user.balance}), 201

@app.route("/users")
def get_users():
    users = run_async(Users.all())
    return jsonify([{"id": u.id, "name": u.username, "balance": u.balance} for u in users])

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        # Дополнительная гарантия закрытия
        cleanup()