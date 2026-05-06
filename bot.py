import telebot
import requests
import os
from telebot import types

# --- ပြင်ဆင်ရန် အပိုင်း ---
# ၁။ သင့် Bot Token (ထည့်ပေးထားပြီးသားဖြစ်သည်)
BOT_TOKEN = "8699185806:AAHioOhJMq-0nO_uYycVkbV4c_xNm_Xd3xY"

# ၂။ သင့် Channel Username (@ သင်္ကေတ ပါရမည်)
CHANNEL_ID = "@termuxguide12" 
# -----------------------

bot = telebot.TeleBot(BOT_TOKEN)

# User က Channel join ထားခြင်း ရှိမရှိ စစ်ဆေးသည့် function
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # အခြေအနေ (status) က left သို့မဟုတ် kicked မဟုတ်ရင် join ထားတယ်လို့ သတ်မှတ်တယ်
        if member.status not in ['left', 'kicked']:
            return True
        return False
    except Exception as e:
        # Bot က channel ထဲမှာ admin မဟုတ်ရင် error တက်တတ်ပါသည်
        print(f"Sub check error: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🌟 *Ultra HD TikTok Downloader*\n\n"
        "Bot ကို အသုံးပြုဖို့ ကျွန်ုပ်တို့ရဲ့ Channel ကို အရင် Join ပေးရပါမယ်။\n"
        "Join ပြီးရင်တော့ TikTok Link ပို့ပြီး ဒေါင်းလုဒ်ဆွဲနိုင်ပါပြီ။"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    url = message.text

    # ၁။ Channel join ထားခြင်း ရှိမရှိ အရင်စစ်ဆေးမယ်
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        # Channel link ကို username မှ ဖန်တီးခြင်း
        clean_channel_name = CHANNEL_ID.replace('@', '')
        join_button = types.InlineKeyboardButton("Join Channel 📢", url=f"https://t.me/{clean_channel_name}")
        markup.add(join_button)
        
        bot.send_message(
            message.chat.id, 
            "⚠️ *Access Denied!*\n\nဒီ Bot ကို သုံးနိုင်ဖို့ ကျွန်ုပ်တို့ရဲ့ Channel ကို အရင် Join ပေးပါ။ Join ပြီးမှ Link ကို ပြန်ပို့ပေးပါ။", 
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    # ၂။ TikTok Link စစ်ဆေးခြင်း
    if "tiktok.com" in url:
        msg = bot.reply_to(message, "🚀 TikTok Video Watermark ဖျောက်နေသည်...")
        try:
            # TikWM API အသုံးပြုခြင်း
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            res = requests.get(api_url).json()
            
            if res.get('code') == 0:
                data = res['data']
                video_url = data.get('play') # အသံကြည်လင်သော quality
                
                bot.send_video(
                    message.chat.id, 
                    video_url, 
                    caption="✅ *Ultra HD ဗီဒီယို ရပါပြီ!*\n\nCreated by: [Taro](https://t.me/Yes_is_me_Taro)", 
                    parse_mode="Markdown"
                )
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ Link မှားနေပါသည်။ https နဲ့စတဲ့ link အမှန်ကိုပဲ ပို့ပေးပါ။", message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text("⚠️ စနစ်ချို့ယွင်းချက်ရှိနေပါသည်။ ခဏနေမှ ပြန်စမ်းပါ။", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "TikTok Link သီးသန့်သာ ပို့ပေးပါခင်ဗျာ။")

# Bot ကို စတင် run ခြင်း
print("Bot is running...")
bot.polling(none_stop=True)
