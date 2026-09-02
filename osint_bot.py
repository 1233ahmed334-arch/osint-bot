import os
import urllib.parse
import phonenumbers
from phonenumbers import geocoder, carrier
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8696755781:AAGRTVtNFZrA2APHkS1wNo7iCP6Jg76j6p8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🔥 *Welcome to Ultimate OSINT Bot* 🔥\n\n"
        "أهلاً بك! أرسل لي الأوامر التالية للفحص المباشر:\n\n"
        "📱 `/phone +201012345678` - فحص رقم هاتف + Truecaller Dorks\n"
        "✉️ `/email target@gmail.com` - فحص حسابات وتصميم تسريبات الإيميل\n"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def phone_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ يرجى إدخال الرقم مع كود الدولة:\nمثال: `/phone +201012345678`", parse_mode="Markdown")
        return

    phone = context.args[0]
    safe_phone = urllib.parse.quote(phone)
    await update.message.reply_text(f"⏳ جاري فحص الرقم `{phone}`...", parse_mode="Markdown")

    parsed_info = ""
    try:
        parsed_num = phonenumbers.parse(phone)
        country = geocoder.description_for_number(parsed_num, "ar")
        net_carrier = carrier.name_for_number(parsed_num, "en")
        parsed_info = f"📍 *الدولة:* {country}\n📶 *الشبكة:* {net_carrier if net_carrier else 'غير معروفة'}\n\n"
    except Exception:
        parsed_info = "📍 *البيانات الأساسية:* تعذر الجلب\n\n"

    truecaller_search = f"https://www.truecaller.com/search/eg/{safe_phone}"
    
    dorks_msg = (
        f"🎯 *نتائج فحص الهاتف:* `{phone}`\n\n"
        f"{parsed_info}"
        f"🔍 *روابط الكشف المباشر (Truecaller & Dorks):*\n"
        f"▪️ [Truecaller Direct Search]({truecaller_search})\n"
        f"▪️ [Google Truecaller Dork](https://www.google.com/search?q='{safe_phone}'+Truecaller)\n"
        f"▪️ [WhatsApp Direct Chat](https://wa.me/{phone.replace('+', '')})\n"
        f"▪️ [Facebook Search](https://www.google.com/search?q=site:facebook.com+'{safe_phone}')\n"
        f"▪️ [Telegram Search](https://www.google.com/search?q=site:telegram.me+'{safe_phone}')"
    )

    await update.message.reply_text(dorks_msg, parse_mode="Markdown", disable_web_page_preview=True)

async def email_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ يرجى كتابة الإيميل:\nمثال: `/email test@gmail.com`", parse_mode="Markdown")
        return

    email = context.args[0]
    await update.message.reply_text(f"⏳ جاري فحص الحسابات المرتبطة بالإيميل `{email}` عبر Holehe...", parse_mode="Markdown")
    
    os.system(f'holehe "{email}" --only-used > email_res.txt')
    
    if os.path.exists("email_res.txt"):
        with open("email_res.txt", "r") as f:
            res = f.read()
        os.remove("email_res.txt")
    else:
        res = "لا توجد نتائج أو تعذر الفحص."

    msg = f"📧 *نتائج فحص الإيميل:* `{email}`\n\n```\n{res[:3500]}\n```"
    await update.message.reply_text(msg, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("phone", phone_scan))
    app.add_handler(CommandHandler("email", email_scan))

    print("🤖 OSINT Telegram Bot is running live...")
    app.run_polling()

if __name__ == "__main__":
    main()
