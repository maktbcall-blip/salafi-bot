import os
from telethon import TelegramClient, events
from telethon.tl.custom import Button

# بيانات التوثيق (تم تحديث توكن البوت الجديد)
API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8842393887:AAGnUuwXSwDE7pUP_Ohgw7oolf87BCCjoV0")

# الآيدي الشخصي للمشرف
ADMIN_ID = int(os.environ.get("ADMIN_ID", 8779419591))

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# الأقسام الشرعية
CATEGORIES = {
    "cat_1": "القرآن الكريم وعلومه",
    "cat_2": "التوحيد والعقيدة",
    "cat_3": "الفقه وأصوله",
    "cat_4": "الحديث وعلومه",
    "cat_5": "السيرة والتاريخ الإسلامي",
    "cat_6": "الآداب والأخلاق والرقائق والأدعية والأذكار",
    "cat_7": "محاربة البدع والردود",
    "cat_8": "الفرق الضالة والمبتدعة",
    "cat_9": "محاربة الإلحاد",
    "cat_10": "الرد على الشبهات",
    "cat_11": "فوائد ونصائح متنوعة",
    "cat_12": "السير والتراجم"
}

BASE_DIR = "books"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

for cat_name in CATEGORIES.values():
    cat_path = os.path.join(BASE_DIR, cat_name)
    if not os.path.exists(cat_path):
        os.makedirs(cat_path)

def get_sections_keyboard():
    buttons = []
    row = []
    for key, name in CATEGORIES.items():
        cat_path = os.path.join(BASE_DIR, name)
        count = len(os.listdir(cat_path)) if os.path.exists(cat_path) else 0
        btn_text = f"{name} ({count})"
        row.append(Button.inline(btn_text, data=key.encode('utf-8')))
        if len(row) == 1:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return buttons

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "مرحباً بك في بوت المكتبة السلفي 📚\n\n"
        "اختر القسم المطلوب من الأزرار بالأسفل لتصفح الكتب:",
        buttons=get_sections_keyboard()
    )

@client.on(events.NewMessage(pattern='/sections'))
async def list_sections(event):
    await event.respond(
        "📂 **أقسام المكتبة السلفية:**",
        buttons=get_sections_keyboard()
    )

@client.on(events.NewMessage(func=lambda e: e.is_private and e.sender_id == ADMIN_ID and e.document))
async def save_new_book(event):
    try:
        default_cat = list(CATEGORIES.values())[0]
        cat_path = os.path.join(BASE_DIR, default_cat)
        if not os.path.exists(cat_path):
            os.makedirs(cat_path)
            
        file_path = await event.download_media(file=cat_path)
        file_name = os.path.basename(file_path)
        await event.respond(f"✅ تم حفظ الكتاب في قسم ({default_cat}) بنجاح:\n`{file_name}`")
    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء حفظ الكتاب: {str(e)}")

@client.on(events.NewMessage(pattern='/delete'))
async def delete_book(event):
    if event.sender_id != ADMIN_ID:
        await event.respond("❌ عذراً، هذا الأمر مخصص للمشرف فقط.")
        return
        
    text = event.text.replace('/delete', '').strip()
    if not text:
        await event.respond("⚠️ يرجى كتابة اسم أو رقم الكتاب المراد حذفه بعد الأمر.")
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
        await event.respond("❌ لم يتم العثور على الكتاب المراد حذفه.")

@client.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('cat_'):
        cat_name = CATEGORIES.get(data)
        if not cat_name:
            await event.answer("القسم غير موجود", alert=True)
            return
            
        cat_path = os.path.join(BASE_DIR, cat_name)
        files = sorted(os.listdir(cat_path)) if os.path.exists(cat_path) else []
        
        if not files:
            await event.edit(f"📁 قسم **{cat_name}** فارغ حالياً.", buttons=[[Button.inline("⬅️ عودة للأقسام", data=b"back_to_home")]])
            return
            
        response = f"📂 **كتب قسم ({cat_name}):**\n\n"
        for i, file in enumerate(files, 1):
            clean_name = file.replace("_", " ").replace('.pdf', '')
            response += f"`{i}.` {clean_name}\n"
        response += "\n💡 أرسل رقم الكتاب المطلوب برقم صحيح لإرساله لك."
        
        await event.edit(response, buttons=[[Button.inline("⬅️ عودة للأقسام", data=b"back_to_home")]])
        
    elif data == b'back_to_home':
        await event.edit(
            "مرحباً بك في بوت المكتبة السلفي 📚\n\nاختر القسم المطلوب من الأزرار بالأسفل:",
            buttons=get_sections_keyboard()
        )

@client.on(events.NewMessage(func=lambda e: e.is_private and not e.text.startswith('/')))
async def handle_user_input(event):
    text = event.text.strip()
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
        await event.respond("❌ الكتاب غير موجود. استخدم الأزرار لتصفح الأقسام.")

print("Bot is running...")
client.run_until_disconnected()
