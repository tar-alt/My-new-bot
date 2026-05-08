import telebot
import requests
from telebot import types

# --- API CONFIG ---
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
WEB_APP_URL = "https://tar-alt.github.io/Test-Cam/" 

bot = telebot.TeleBot(BOT_TOKEN)
pending_videos = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tiktok(message):
    user_id = message.chat.id
    pending_videos[user_id] = message.text
    
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", web_app=web_app)
    markup.add(verify_btn)
    
    bot.reply_to(message, "⚠️ *Verification Required*\n\nလူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးပါ။", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "✅ Verification_Success")
def process_download(message):
    user_id = message.chat.id
    if user_id in pending_videos:
        url = pending_videos[user_id]
        bot.send_message(user_id, "🚀 Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
        
        try:
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            res = requests.get(api_url).json()
            if res.get('code') == 0:
                video_url = res['data'].get('play') 
                bot.send_video(user_id, video_url, caption="✅ *Done!*")
            else:
                bot.send_message(user_id, "❌ Error: ဗီဒီယို ရှာမတွေ့ပါ။")
        except:
            bot.send_message(user_id, "⚠️ စနစ်ချို့ယွင်းချက် ရှိနေပါသည်။")
        
        del pending_videos[user_id]

bot.infinity_polling()
