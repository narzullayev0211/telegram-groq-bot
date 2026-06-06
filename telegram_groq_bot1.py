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
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ======================

# XOTIRA

# ======================

user_memory = {}

MAX_HISTORY = 10

# ======================

# START

# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
"Salom! Men Groq AI botman. Savolingizni yuboring."
)

# ======================

# CLEAR MEMORY

# ======================

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
user_id = update.effective_user.id

if user_id in user_memory:
    del user_memory[user_id]

await update.message.reply_text(
    "Xotira tozalandi."
)
```

# ======================

# CHAT

# ======================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
user_id = update.effective_user.id
user_text = update.message.text

if user_id not in user_memory:

    user_memory[user_id] = [
        {
            "role": "system",
            "content": (
                "Sen professional sun'iy intellekt yordamchisan. "
                "O'zbek tilida aniq va tushunarli javob ber. "
                "Gidrotexnika, suv xo'jaligi, gidravlika, "
                "gruntli to'g'onlar va ilmiy maqolalar "
                "bo'yicha ham yordam bera olasan."
            )
        }
    ]

user_memory[user_id].append(
    {
        "role": "user",
        "content": user_text
    }
)

try:

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=user_memory[user_id],
        temperature=0.7,
        max_tokens=2048
    )

    answer = response.choices[0].message.content

    user_memory[user_id].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    if len(user_memory[user_id]) > MAX_HISTORY * 2:
        user_memory[user_id] = (
            [user_memory[user_id][0]]
            + user_memory[user_id][-MAX_HISTORY * 2:]
        )

    if len(answer) > 4000:
        for i in range(0, len(answer), 4000):
            await update.message.reply_text(answer[i:i+4000])
    else:
        await update.message.reply_text(answer)

except Exception as e:
    await update.message.reply_text(
        f"Xatolik:\n{e}"
    )
```

# ======================

# MAIN

# ======================

def main():

```
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("clear", clear))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        chat
    )
)

print("Bot ishga tushdi...")

app.run_polling()
```

if **name** == "**main**":
asyncio.set_event_loop(asyncio.new_event_loop())
main()
