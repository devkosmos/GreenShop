import asyncio
import signal
import sys
from flask import Flask, jsonify, render_template
from tortoise import Tortoise
from database.models.user import Users
from database.models.catalog import Category, Products

app = Flask(__name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Инициализация БД
async def init_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["database.models"]}
    )
    await Tortoise.generate_schemas()

def run_async(coro):
    return loop.run_until_complete(coro)

run_async(init_db())

# Корректное завершение
def shutdown():
    print("\nЗакрытие БД...")
    run_async(Tortoise.close_connections())
    sys.exit(0)

signal.signal(signal.SIGINT, lambda s, f: shutdown())

@app.route("/")
def home():
    user = run_async(Users.create(username="Muhkhamed", balance=700))
    return jsonify(id=user.id, name=user.username, balance=user.balance)

@app.route("/page")
def main():
    discord = run_async(Category.create(name="DiscordX"))
    discord_nitro = run_async(Products.create(title="Discord Nitro", description="Premium subscription", price=499, category_id=discord))
    return render_template("home.html", category=discord.name)
if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        shutdown()