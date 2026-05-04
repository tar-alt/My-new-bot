import telebot
import requests
import os

# GitHub Secrets ထဲက Token ကို လှမ်းယူခြင်း
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🌟 Ultra HD & High Volume TikTok Downloader အဆင်သင့်ဖြစ်ပါပြီ။")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "tiktok.com" in url:
        msg = bot.reply_to(message, "🚀 TikTok Video Watermark ဖျောက်နေသည်...")
        try:
            # HD Quality ရရန် hd=1 ထည့်သွင်းထားသည်
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            res = requests.get(api_url).json()
            
            if res.get('code') == 0:
                data = res['data']
                
                # Black Screen မဖြစ်စေဘဲ အသံကျယ်ကျယ်ရရန် 'play' ကို အဓိကထားသုံးပါမည်
                # 'play' သည် Compatibility အကောင်းဆုံးဖြစ်ပြီး အသံ Bitrate လည်း မြင့်သည်
                video_url = data.get('play') 
                
                bot.send_video(
                    message.chat.id, 
                    video_url, 
                    caption="✅ Ultra HD ဗီဒီယို ရပါပြီ!\nCreated by: [Taro](https://t.me/Yes_is_me_Taro)", 
                    parse_mode="Markdown"
                )
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ Link မှားနေပါသည်။ https နဲ့စတဲ့နေရာကစပြီးပို့ပေးပါ ၎င်းရှေ့တွင်တခြားစာလုံးများမပါရ။", message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text("⚠️ စနစ်ချို့ယွင်းချက်ရှိနေပါသည်။ ခဏနေမှ ပြန်စမ်းပါ။", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "TikTok Link ပဲ ပို့ပေးပါခင်ဗျာ။")

bot.polling(none_stop=True)
