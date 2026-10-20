import os
from telethon import TelegramClient, events

# بيانات التوثيق الخاصة بك
API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8842393887:AAHWH5Vn0Ck5jg8TWQMmx6jIUm8cDcIWLyw")

# الآيدي الشخصي الخاص بك بصلاحية المشرف الكاملة لرفع الكتب
ADMIN_ID = int(os.environ.get("ADMIN_ID", 8779419591))

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# مجلد لحفظ الكتب المستلمة سحابياً
BOOKS_DIR = "books"
if not os.path.exists(BOOKS_DIR):
    os.makedirs(BOOKS_DIR)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "مرحباً بك في بوت المكتبة السلفي 📚\n\n"
        "يمكنك استخدام الأوامر التالية:\n"
        "▫️ /books - لعرض قائمة الكتب المرتبة.\n"
        "▫️ أرسل رقم الكتاب (مثلاً: 2) ليقوم البوت بإرساله لك فوراً!\n\n"
        "💡 ملاحظة: رفع الكتب مخصص للمشرف فقط."
    )

# استقبال الكتب وإضافتها تلقائياً (مخصص لك أنت فقط عبر ADMIN_ID)
@client.on(events.NewMessage(func=lambda e: e.is_private and e.sender_id == ADMIN_ID and e.document))
async def save_new_book(event):
    try:
        if not os.path.exists(BOOKS_DIR):
            os.makedirs(BOOKS_DIR)
        file_path = await event.download_media(file=BOOKS_DIR)
        file_name = os.path.basename(file_path)
        await event.respond(f"✅ تم حفظ الكتاب بنجاح وتمت إضافته للمكتبة:\n`{file_name}`")
    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء حفظ الكتاب: {str(e)}")

# أمر لعرض الكتب المتاحة بطريقة مرتبة ونظيفة
@client.on(events.NewMessage(pattern='/books'))
async def list_books(event):
    if not os.path.exists(BOOKS_DIR):
        os.makedirs(BOOKS_DIR)
    files = sorted(os.listdir(BOOKS_DIR))
    if not files:
        await event.respond("📁 لا توجد كتب مضافة في المكتبة حالياً.")
        return
    
    response = "📚 **قائمة الكتب المتاحة في المكتبة:**\n\n"
    for i, file in enumerate(files, 1):
        clean_name = file.replace("_", " ").replace(".pdf", "")
        response += f"`{i}.` {clean_name}\n"
    
    response += "\n💡 **أرسل رقم الكتاب فقط (مثل: 2) وسيقوم البوت بإرساله لك فوراً!**"
    await event.respond(response)

# دالة الاستجابة عند إرسال رقم الكتاب أو جزء من اسمه ليتم إرساله تلقائياً للمستخدم
@client.on(events.NewMessage(func=lambda e: e.is_private and not e.text.startswith('/')))
async def send_book_to_user(event):
    if not os.path.exists(BOOKS_DIR):
        os.makedirs(BOOKS_DIR)
    files = sorted(os.listdir(BOOKS_DIR))
    if not files:
        return
    
    text = event.text.strip()
    target_file = None
    
    if text.isdigit():
        index = int(text) - 1
        if 0 <= index < len(files):
            target_file = files[index]
    else:
        for file in files:
            if text.lower() in file.lower():
                target_file = file
                break
                
    if target_file:
        file_path = os.path.join(BOOKS_DIR, target_file)
        await event.respond(f"📖 تفضل كتاب: **{target_file.replace('_', ' ').replace('.pdf', '')}**")
        await client.send_file(event.chat_id, file_path)
    else:
        await event.respond("❌ الكتاب المطلوب غير موجود. استخدم الأمر /books لعرض القائمة الصحيحة.")

print("Bot is running...")
client.run_until_disconnected()
