from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from groq import Groq
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ======================
# START
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men Groq AI botman. Savolingizni yuboring."
    )

# ======================
# CHAT
# ======================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen professional sun'iy intellekt yordamchisan. "
                        "O'zbek tilida aniq va tushunarli javob ber."
                    )
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            temperature=0.7,
            max_tokens=2048
        )

        answer = response.choices[0].message.content

        if len(answer) > 4000:
            for i in range(0, len(answer), 4000):
                await update.message.reply_text(answer[i:i+4000])
        else:
            await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            f"Xatolik:\n{e}"
        )

# ======================
# MAIN
# ======================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    print("Bot ishga tushdi...")

    app.run_polling()

import asyncio

if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    main()
