import os
import aiohttp
from aiohttp import web
import asyncio
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN")

async def handle(request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET_TOKEN:
        return web.Response(status=403, text="Forbidden")
    try:
        data = await request.json()
        # Основная логика реакции бота
        message = data.get("message", {}).get("text", "").lower()
        chat_id = data.get("message", {}).get("chat", {}).get("id")

        if message and chat_id:
            async with aiohttp.ClientSession() as session:
                await session.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": "🤖 Nyra activated. I see you."}
                )
        return web.Response(status=200, text="ok")
    except Exception as e:
        return web.Response(status=500, text=str(e))

app = web.Application()
app.router.add_post("/", handle)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))