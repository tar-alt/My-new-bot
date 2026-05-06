import telebot
import requests
import os
from telebot import types

# --- ပြင်ဆင်ရန် အပိုင်း ---
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
CHANNEL_ID = "@termuxguide12" # ဒီနေရာမှာ သင့် channel name ကို အမှန်ပြင်ပါ
# -----------------------

bot = telebot.TeleBot(BOT_TOKEN)

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ['left', 'kicked']:
            return True
        return False
    except Exception:
        return False

# --- ဒီအပိုင်းကို အဓိက ပြင်ဆင်ထားပါတယ် ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Join Button ပြုလုပ်ခြင်း
    markup = types.InlineKeyboardMarkup()
    clean_name = CHANNEL_ID.replace('@', '')
    markup.add(types.InlineKeyboardButton("Join Channel 📢", url=f"https://t.me/{clean_name}"))
    
    welcome_text = (
        "🌟 *Ultra HD TikTok Downloader*\n\n"
        "Bot ကို အသုံးပြုဖို့ ကျွန်ုပ်တို့ရဲ့ Channel ကို အရင် Join ပေးရပါမယ်။\n"
        "Join ပြီးရင်တော့ TikTok Link ပို့ပြီး ဒေါင်းလုဒ်ဆွဲနိုင်ပါပြီ။"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    url = message.text

    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        clean_name = CHANNEL_ID.replace('@', '')
        markup.add(types.InlineKeyboardButton("Join Channel 📢", url=f"https://t.me/{clean_name}"))
        
        bot.send_message(
            message.chat.id, 
            "⚠️ *Access Denied!*\n\nဒီ Bot ကို သုံးနိုင်ဖို့ ကျွန်ုပ်တို့ရဲ့ Channel ကို အရင် Join ပေးပါ။ Join ပြီးမှ Link ကို ပြန်ပို့ပေးပါ။", 
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    if "tiktok.com" in url:
        msg = bot.reply_to(message, "🚀 TikTok Video Watermark ဖျောက်နေသည်...")
        try:
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            res = requests.get(api_url).json()
            if res.get('code') == 0:
                video_url = res['data'].get('play') 
                bot.send_video(
                    message.chat.id, 
                    video_url, 
                    caption="✅ *Ultra HD ဗီဒီယို ရပါပြီ!*\n\nCreated by: [Taro](https://t.me/Yes_is_me_Taro)", 
                    parse_mode="Markdown"
                )
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ Link မှားနေပါသည်။", message.chat.id, msg.message_id)
        except:
            bot.edit_message_text("⚠️ စနစ်ချို့ယွင်းချက်ရှိနေပါသည်။", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "TikTok Link ပဲ ပို့ပေးပါ။")

bot.polling(none_stop=True)
        
