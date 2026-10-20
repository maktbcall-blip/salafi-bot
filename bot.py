import os
from telethon import TelegramClient, events

# بيانات التوثيق
API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8842393887:AAHWH5Vn0Ck5jg8TWQMmx6jIUm8cDcIWLyw")

# الآيدي الشخصي للمشرف
ADMIN_ID = int(os.environ.get("ADMIN_ID", 8779419591))

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# الأقسام الشرعية المأخوذة من المكتبة
CATEGORIES = {
    "1": "القرآن الكريم وعلومه",
    "2": "التوحيد والعقيدة",
    "3": "الفقه وأصوله",
    "4": "الحديث وعلومه",
    "5": "السيرة والتاريخ الإسلامي",
    "6": "الآداب والأخلاق والرقائق والأدعية والأذكار",
    "7": "محاربة البدع والردود",
    "8": "الفرق الضالة والمبتدعة",
    "9": "محاربة الإلحاد",
    "10": "الرد على الشبهات",
    "11": "فوائد ونصائح متنوعة",
    "12": "السير والتراجم"
}

# إنشاء المجلدات الرئيسية والأقسام تلقائياً
BASE_DIR = "books"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

for cat_name in CATEGORIES.values():
    cat_path = os.path.join(BASE_DIR, cat_name)
    if not os.path.exists(cat_path):
        os.makedirs(cat_path)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "مرحباً بك في بوت المكتبة السلفي 📚\n\n"
        "الأوامر المتاحة:\n"
        "▫️ /sections - لعرض أقسام المكتبة.\n"
        "▫️ /books - لعرض كافة الكتب.\n"
        "▫️ لحذف كتاب (للمشرف): أرسل /delete ثم رقم الكتاب.\n\n"
        "💡 ملاحظة: رفع الكتب مخصص للمشرف فقط."
    )

@client.on(events.NewMessage(pattern='/sections'))
async def list_sections(event):
    response = "📂 **أقسام المكتبة السلفية:**\n\n"
    for key, name in CATEGORIES.items():
        cat_path = os.path.join(BASE_DIR, name)
        count = len(os.listdir(cat_path)) if os.path.exists(cat_path) else 0
        response += f"`{key}.` {name} ({count} كتاب)\n"
    
    response += "\n💡 لعرض كتب قسم معين، أرسل رقم القسم (مثلاً: `2` لعرض كتب التوحيد والعقيدة)."
    await event.respond(response)

@client.on(events.NewMessage(func=lambda e: e.is_private and e.sender_id == ADMIN_ID and e.document))
async def save_new_book(event):
    try:
        default_cat = list(CATEGORIES.values())[0]
        cat_path = os.path.join(BASE_DIR, default_cat)
        if not os.path.exists(cat_path):
            os.makedirs(cat_path)
            
        file_path = await event.download_media(file=cat_path)
        file_name = os.path.basename(file_path)
        await event.respond(f"✅ تم حفظ الكتاب في قسم ({default_cat}) بنجاح:\n`{file_name}`\n\nيمكنك نقله يدوياً أو سيتم تطويره لاحقاً لاختيار القسم.")
    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء حفظ الكتاب: {str(e)}")

@client.on(events.NewMessage(pattern='/delete'))
async def delete_book(event):
    if event.sender_id != ADMIN_ID:
        await event.respond("❌ عذراً، هذا الأمر مخصص للمشرف فقط.")
        return
        
    text = event.text.replace('/delete', '').strip()
    if not text:
        await event.respond("⚠️ يرجى كتابة رقم الكتاب المراد حذفه بعد الأمر. مثال:\n`/delete 3`")
        return
        
    all_files = []
    for cat_name in CATEGORIES.values():
        cat_path = os.path.join(BASE_DIR, cat_name)
        if os.path.exists(cat_path):
            for f in os.listdir(cat_path):
                all_files.append((f, cat_path))
                
    target_file = None
    target_path = None
    
    if text.isdigit():
        index = int(text) - 1
        if 0 <= index < len(all_files):
            target_file, target_path = all_files[index]
    else:
        for f, p in all_files:
            if text.lower() in f.lower():
                target_file, target_path = f, p
                break
                
    if target_file:
        full_path = os.path.join(target_path, target_file)
        os.remove(full_path)
        await event.respond(f"🗑️ تم حذف الكتاب بنجاح:\n`{target_file.replace('_', ' ').replace('.pdf', '')}`")
    else:
        await event.respond("❌ لم يتم العثور على الكتاب المراد حذفه. تأكد من الرقم عبر /books.")

@client.on(events.NewMessage(pattern='/books'))
async def list_books(event):
    response = "📚 **فهرس كتب المكتبة السلفي:**\n\n"
    global_index = 1
    has_books = False
    
    for cat_name in CATEGORIES.values():
        cat_path = os.path.join(BASE_DIR, cat_name)
        if os.path.exists(cat_path):
            files = sorted(os.listdir(cat_path))
            if files:
                has_books = True
                response += f"📂 **{cat_name}:**\n"
                for file in files:
                    clean_name = file.replace("_", " ").replace(".pdf", "")
                    response += f"   `{global_index}.` {clean_name}\n"
                    global_index += 1
                response += "\n"
                
    if not has_books:
        await event.respond("📁 لا توجد كتب مضافة في المكتبة حالياً.")
        return
        
    response += "💡 **أرسل رقم الكتاب فقط (مثل: 2) ليقوم البوت بإرساله لك فوراً!**"
    await event.respond(response)

@client.on(events.NewMessage(func=lambda e: e.is_private and not e.text.startswith('/')))
async def handle_user_input(event):
    text = event.text.strip()
    
    if text in CATEGORIES:
        cat_name = CATEGORIES[text]
        cat_path = os.path.join(BASE_DIR, cat_name)
        files = sorted(os.listdir(cat_path)) if os.path.exists(cat_path) else []
        
        if not files:
            await event.respond(f"📁 قسم **{cat_name}** فارغ حالياً.")
            return
            
        response = f"📂 **كتب قسم ({cat_name}):**\n\n"
        for i, file in enumerate(files, 1):
            clean_name = file.replace("_", " ").replace('.pdf', '')
            response += f"`{i}.` {clean_name}\n"
        response += "\n💡 أرسل رقم الكتاب المطلوب لإرساله."
        await event.respond(response)
        return

    all_files = []
    for cat_name in CATEGORIES.values():
        cat_path = os.path.join(BASE_DIR, cat_name)
        if os.path.exists(cat_path):
            for f in sorted(os.listdir(cat_path)):
                all_files.append((f, cat_path))
                
    if not all_files:
        return
        
    target_file = None
    target_path = None
    
    if text.isdigit():
        index = int(text) - 1
        if 0 <= index < len(all_files):
            target_file, target_path = all_files[index]
    else:
        for f, p in all_files:
            if text.lower() in f.lower():
                target_file, target_path = f, p
                break
                
    if target_file:
        file_path = os.path.join(target_path, target_file)
        await event.respond(f"📖 تفضل كتاب: **{target_file.replace('_', ' ').replace('.pdf', '')}**")
        await client.send_file(event.chat_id, file_path)
    else:
        await event.respond("❌ الكتاب أو القسم غير موجود. استخدم /sections لعرض الأقسام أو /books لعرض الكتب.")

print("Bot is running...")
client.run_until_disconnected()
