import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

CARD_NUMBER = "6104 3379 5494 2122"
CARD_NAME = "قاسم زاده"

bot = telebot.TeleBot(BOT_TOKEN)

def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=["start"])
def start(message):
    if not is_user_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        markup.add(btn)
        bot.send_message(message.chat.id, "برای استفاده از ربات ابتدا در کانال عضو شوید 👇", reply_markup=markup)
        return

    msg = f"🎉 خوش آمدید به Maxi Vpn
برای خرید VPN لطفاً مبلغ مورد نظر را به شماره کارت زیر واریز کرده و رسید را ارسال کنید:

💳 شماره کارت: {CARD_NUMBER}
👤 به نام: {CARD_NAME}"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(content_types=["photo"])
def handle_payment_receipt(message):
    if not is_user_subscribed(message.from_user.id):
        return
    caption = f"📥 رسید پرداخت از کاربر:
👤 {message.from_user.first_name} (@{message.from_user.username})
🆔 {message.from_user.id}"
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)
    bot.reply_to(message, "رسید شما برای مدیر ارسال شد. پس از بررسی کانفیگ برایتان ارسال می‌شود.")

@bot.message_handler(commands=["panel"])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🔐 پنل مدیریت فعال است.
دستورات آتی در این نسخه ساده دستی انجام می‌گیرد.")
    else:
        bot.reply_to(message, "شما به پنل دسترسی ندارید.")

bot.infinity_polling()
