import telebot
import requests
import os

# GitHub Secrets ထဲက Token ကို လှမ်းယူမှာဖြစ်ပါတယ်
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "⚡ GitHub Server ပေါ်မှာ Bot အလုပ်လုပ်နေပါပြီ။ Link ပို့ပေးပါ။")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "tiktok.com" in url:
        msg = bot.reply_to(message, "⏳ ဗီဒီယို ရှာနေပါတယ်...")
        try:
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()
            if response.get('code') == 0:
                video_url = response['data']['play']
                bot.send_video(message.chat.id, video_url, caption="Done! ✅")
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ Link မှားနေပါသည်။", message.chat.id, msg.message_id)
        except:
            bot.edit_message_text("⚠️ Error တက်သွားပါသည်။", message.chat.id, msg.message_id)

bot.polling(none_stop=True)
