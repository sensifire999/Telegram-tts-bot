import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

# Tokens ko environment variables se read karenge
TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

# HuggingFace TTS Model
# English ke liye: facebook/mms-tts-eng
# Hindi ke liye: facebook/mms-tts-hin
MODEL = "facebook/mms-tts-eng"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# HuggingFace API call
def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.content

# Telegram handler
async def tts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    audio_bytes = query({"inputs": text})

    # Save as file
    with open("voice.wav", "wb") as f:
        f.write(audio_bytes)

    await update.message.reply_voice(voice=open("voice.wav", "rb"))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tts))
    app.run_polling()

if __name__ == "__main__":
    main()
