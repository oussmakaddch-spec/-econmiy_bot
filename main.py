import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- 1. سيرفر Flask للحفاظ على عمل البوت ---
app = Flask(__name__)

@app.route('/')
def home():
    return "EcomSpy Bot is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 2. بيانات المنتجات المربحة (Winning Products) ---
WINNING_PRODUCTS = [
    {
        "title": "مصحح القامة الذكي (Posture Corrector)",
        "price": "3500 دج",
        "margin": "ربح متوقع: 1800 دج لكل قطعة",
        "desc": "منتج يحل مشكلة آلام الظهر، عليه طلب كبير في السوق الجزائري ومناسب لإعلانات الفيس بوك.",
        "ad_copy": "تخلص من آلام الظهر والرقبة فوراً! الحزام الذكي ينبهك باهتزاز خفيف عند انحناء ظهرك. اطلبه الآن والتوصيل متوفر 58 ولاية!",
        "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500"
    },
    {
        "title": "مضخة المياه الكهربائية الشارجبيل",
        "price": "1900 دج",
        "margin": "ربح متوقع: 900 دج لكل قطعة",
        "desc": "منتج نيش بامتياز، سهل التسويق للعائلات والمكاتب، حجمه صغير وتوصيله خفيف.",
        "ad_copy": "اهتني من ثقل قارورات الماء! المضخة الكهربائية الذكية تشحن بـ USB وتفرغ الماء بضغطة زر واحدة. اطلبها الآن!",
        "image": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=500"
    }
]

# --- 3. أوامر البوت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "🔥 **أهلاً بك في بوت اقتناص المنتجات المربحة (EcomSpy)!**\n\n"
        "أنا هنا لمساعدتك في العثور على أفضل المنتجات ذات هامش الربح العالي للسوق الجزائري.\n\n"
        "اضغط على الأمر /winning_product للحصول على منتج مربح جديد مع نص الإعلان!"
    )
    await update.message.reply_text(welcome_msg, parse_mode="Markdown")

async def winning_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    product = random.choice(WINNING_PRODUCTS)
    
    caption = (
        f"🎯 **منتج مربح جديد (Winning Product):**\n\n"
        f"📦 **الاسم:** {product['title']}\n"
        f"💰 **سعر البيع المقترح:** {product['price']}\n"
        f"📈 **هامش الربح:** {product['margin']}\n\n"
        f"📝 **الوصف:** {product['desc']}\n\n"
        f"📣 **نص إعلاني جاهز (Ad Copy):**\n`{product['ad_copy']}`"
    )
    
    keyboard = [
        [InlineKeyboardButton("📦 طلب المورد / تفاصيل تفصيلية", url="https://t.me/your_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=product['image'],
        caption=caption,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# --- 4. تشغيل التطبيق ---
if __name__ == '__main__':
    # تشغيل سيرفر الـ Web في Thread منفصل
    t = threading.Thread(target=run_flask)
    t.start()
    
    # حط التوكن تاع البوت تاعك هنا
    BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
    
    # تشغيل بوت تليجرام
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("winning_product", winning_product))
    
    print("⚡️ البوت شغال الآن بنجاح...")
    application.run_polling()
