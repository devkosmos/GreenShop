from flask import Flask, jsonify, render_template
from tortoise import Tortoise
from database.models.user import Users

app = Flask(__name__)

# Инициализация БД один раз при старте
async def setup_db():
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["database.models"]})
    await Tortoise.generate_schemas()

# Синхронная обёртка для асинхронных вызовов
def run_async(coro):
    import asyncio
    return asyncio.run(coro)

# Инициализируем БД
run_async(setup_db())

@app.route("/")
def home():
    user = run_async(Users.create(username="Muhkhamed", balance=700))
    return jsonify({"id": user.id, "name": user.username, "balance": user.balance})

@app.route("/home")
def main():
    return render_template("home.html")

@app.route("/users")
def get_users():
    users = run_async(Users.all())
    return jsonify([{"id": u.id, "name": u.username, "balance": u.balance} for u in users])

if __name__ == "__main__":
    app.run(debug=True)