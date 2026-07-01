import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("8810242954:AAGmlF9QAC7gtOdabIJGaiJCYmE5o5e2_H0")
ADMIN_ID = 6017535013

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# Stores admin message id -> original group message info
message_map = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "✅ Tyler Durden Manual Reply Bot Online!"
    )


async def group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.type not in ["group", "supergroup"]:
        return

    msg = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    text = msg.text

    if not text:
        text = "[Non-text message]"

    info = (
        f"📢 Group : {chat.title}\n"
        f"👤 {user.full_name}\n"
        f"🆔 {user.id}\n\n"
        f"{text}"
    )

    sent = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=info,
    )

    message_map[sent.message_id] = {
        "chat_id": chat.id,
        "reply_to": msg.message_id,
    }
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    msg = update.effective_message

    if not msg.reply_to_message:
        return

    admin_reply_id = msg.reply_to_message.message_id

    if admin_reply_id not in message_map:
        return

    data = message_map[admin_reply_id]

    await context.bot.send_message(
        chat_id=data["chat_id"],
        text=msg.text,
        reply_to_message_id=data["reply_to"],
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text("🏓 Pong!")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "🟢 Bot Online\n"
        "✅ Manual Reply Active"
    )


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("status", status))

    app.add_handler(
        MessageHandler(
            filters.ChatType.GROUPS,
            group_message,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Chat(ADMIN_ID)
            & filters.REPLY
            & filters.TEXT,
            admin_reply,
        )
    )

    print("✅ Tyler Durden Manual Reply Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
