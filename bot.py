import telebot
import requests
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🌟 Ultra HD TikTok Downloader အဆင်သင့်ဖြစ်ပါပြီ သင်Downloadလုပ်ချင်‌သော TikTok Video Link ပို့ပေးပါ။")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "tiktok.com" in url:
        msg = bot.reply_to(message, "🚀 High-Quality ဖြင့်ဗီဒီယိုကို ပို့ပေးနေပါတယ်...")
        try:
            # HD=1 ထည့်သွင်းပြီး Quality အမြင့်ဆုံး တောင်းဆိုခြင်း
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            response = requests.get(api_url).json()
            
            if response.get('code') == 0:
                data = response['data']
                # hdplay ရှိလျှင် သုံးမည်၊ မရှိလျှင် play ကို သုံးမည်
                video_url = data.get('hdplay') or data.get('play')
                
                # ဗီဒီယိုပို့သည့်နေရာ (Hyperlink နာမည်အတိုဖြင့်)
                bot.send_video(
                    message.chat.id, 
                    video_url, 
                    caption="✅ Ultra HD ဖြင့်ပြင်ထား‌သောဗီဒီယို ရပါပြီ!\nCreated by: [Taro](https://t.me/Yes_is_me_Taro)", 
                    parse_mode="Markdown"
                )
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ Link မှားနေပါသည်။ https နဲ့စတဲ့နေရာကစပြီးပို့ပေးပါ ၎င်းရှေ့တွင်တခြားစာလုံးများမပါရ။", message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"⚠️ Error: {str(e)}", message.chat.id, msg.message_id)

bot.polling(none_stop=True)
