import os
import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from analyzer import analyze_message

# إعداد التسجيل (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تجاهل الرسائل التي لا تحتوي على نص أو الرسائل من البوتات
    if not update.message or not update.message.text or update.message.from_user.is_bot:
        return

    text = update.message.text
    user = update.message.from_user
    chat_id = update.effective_chat.id

    # تحليل الرسالة
    is_offensive, reason = analyze_message(text)

    if is_offensive:
        try:
            # حساب وقت فك الكتم (بعد 3 ساعات)
            until_date = datetime.now() + timedelta(hours=3)
            
            # تطبيق الكتم (منع إرسال الرسائل)
            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user.id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until_date
            )

            # حذف الرسالة المسيئة
            await update.message.delete()

            # إرسال تنبيه في المجموعة
            response_msg = (
                f"🚫 **إجراء إداري تلقائي**\n\n"
                f"👤 **المستخدم:** {user.mention_html()}\n"
                f"🔒 **العقوبة:** كتم لمدة 3 ساعات + حذف الرسالة\n"
                f"📝 **السبب:** {reason}\n\n"
                f"⚠️ *يرجى الالتزام بقوانين المجموعة وتجنب الشتائم أو الإساءة للأديان.*"
            )
            await context.bot.send_message(chat_id=chat_id, text=response_msg, parse_mode='HTML')
            
            logging.info(f"User {user.id} muted for: {reason}")
            
        except Exception as e:
            logging.error(f"Failed to restrict user: {e}")
            # قد يفشل البوت إذا لم يكن لديه صلاحيات مشرف أو إذا كان المستخدم مشرفاً

if __name__ == '__main__':
    # ملاحظة: يجب توفير TOKEN عبر متغير بيئة TELEGRAM_BOT_TOKEN
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
    else:
        application = ApplicationBuilder().token(token).build()
        
        # معالجة جميع الرسائل النصية في المجموعات
        message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
        application.add_handler(message_handler)
        
        print("Bot is starting...")
        application.run_polling()
