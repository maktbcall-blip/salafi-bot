import os
from telethon import TelegramClient, events
from telethon.tl.custom import Button

# بيانات التوثيق
API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8842393887:AAGnUuwXSwDE7pUP_Ohgw7oolf87BCCjoV0")

# الآيدي الشخصي للمشرف
ADMIN_ID = int(os.environ.get("ADMIN_ID", 8779419591))

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# الأقسام الشرعية مع الكلمات المفتاحية
CATEGORIES = {
    "cat_1": {"name": "القرآن الكريم وعلومه", "keywords": ["قرآن", "تفسير", "مصحف", "تجويد", "قراءات", "القرآن"]},
    "cat_2": {"name": "التوحيد والعقيدة", "keywords": ["توحيد", "عقيدة", "الواسطية", "التمرية", "الأسماء والصفات"]},
    "cat_3": {"name": "الفقه وأصوله", "keywords": ["فقه", "أصول", "أحكام", "صلاة", "زيام", "صيام", "حج", "معاملات"]},
    "cat_4": {"name": "الحديث وعلومه", "keywords": ["حديث", "سنن", "صحيح", "مسند", "اربعين", "الأربعين", "مصطلح"]},
    "cat_5": {"name": "السيرة والتاريخ الإسلامي", "keywords": ["سيرة", "تاريخ", "الغزوات", "الخلافة", "النبيلة"]},
    "cat_6": {"name": "الآداب والأخلاق والرقائق والأدعية والأذكار", "keywords": ["أذكار", "آداب", "الأداب", "الأذكار", "رقائق", "الرقاق", "أخلاق", "دعاء", "التمهيدي"]},
    "cat_7": {"name": "محاربة البدع والردود", "keywords": ["بدع", "بدعة", "ردود", "الرد", "تحذير"]},
    "cat_8": {"name": "الفرق الضالة والمبتدعة", "keywords": ["فرق", "ضالة", "خوارج", "رافضة", "صوفية", "اشاعرة"]},
    "cat_9": {"name": "محاربة الإلحاد", "keywords": ["إلحاد", "ملحدين", "شبهات", "العلم والدين"]},
    "cat_10": {"name": "الرد على الشبهات", "keywords": ["شبهات", "شبهة", "الردود العلمية"]},
    "cat_11": {"name": "فوائد ونصائح متنوعة", "keywords": ["فوائد", "نصائح", "متنوعة", "رسائل", "مفيدة", "طالب", "العلم", "المستوى"]},
    "cat_12": {"name": "السير والتراجم", "keywords": ["تراجم", "ترجمة", "سير", "أعلام", "العلماء", "وفيات"]}
}

BASE_DIR = "books"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

for cat_info in CATEGORIES.values():
    cat_path = os.path.join(BASE_DIR, cat_info["name"])
    if not os.path.exists(cat_path):
        os.makedirs(cat_path)

def get_sections_keyboard():
    buttons = []
    for key, cat_info in CATEGORIES.items():
        name = cat_info["name"]
        cat_path = os.path.join(BASE_DIR, name)
        count = len(os.listdir(cat_path)) if os.path.exists(cat_path) else 0
        btn_text = f"{name} ({count})"
        buttons.append([Button.inline(btn_text, data=key.encode('utf-8'))])
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
        temp_path = await event.download_media(file=BASE_DIR)
        file_name = os.path.basename(temp_path)
        file_lower = file_name.lower()
        
        target_cat = "فوائد ونصائح متنوعة"
        for cat_info in CATEGORIES.values():
            for kw in cat_info["keywords"]:
                if kw in file_lower:
                    target_cat = cat_info["name"]
                    break
            if target_cat != "فوائد ونصائح متنوعة":
                break
                
        correct_cat_path = os.path.join(BASE_DIR, target_cat)
        if not os.path.exists(correct_cat_path):
            os.makedirs(correct_cat_path)
            
        final_path = os.path.join(correct_cat_path, file_name)
        if os.path.exists(temp_path) and temp_path != final_path:
            if os.path.exists(final_path):
                os.remove(final_path)
            os.rename(temp_path, final_path)
            
        await event.respond(f"✅ تم تصنيف وحفظ الكتاب تلقائياً في قسم:\n📂 **{target_cat}**\n\n📄 باسم: `{file_name}`")
    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء حفظ وتصنيف الكتاب: {str(e)}")

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
    for cat_info in CATEGORIES.values():
        cat_path = os.path.join(BASE_DIR, cat_info["name"])
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
    
    if data == 'back_to_home':
        await event.edit(
            "مرحباً بك في بوت المكتبة السلفي 📚\n\nاختر القسم المطلوب من الأزرار بالأسفل:",
            buttons=get_sections_keyboard()
        )
        return
        
    if data.startswith('cat_'):
        cat_info = CATEGORIES.get(data)
        if not cat_info:
            await event.answer("القسم غير موجود", alert=True)
            return
            
        cat_name = cat_info["name"]
        cat_path = os.path.join(BASE_DIR, cat_name)
        files = sorted(os.listdir(cat_path)) if os.path.exists(cat_path) else []
        
        if not files:
            await event.edit(
                f"📁 قسم **{cat_name}** فارغ حالياً.",
                buttons=[[Button.inline("⬅️ عودة للأقسام", data='back_to_home')]]
            )
            return
            
        book_buttons = []
        for file in files:
            clean_name = file.replace("_", " ").replace('.pdf', '')
            book_buttons.append([Button.inline(f"📖 {clean_name}", data=f"book_{file[:40]}".encode('utf-8'))])
            
        book_buttons.append([Button.inline("⬅️ عودة للأقسام", data='back_to_home')])
        
        await event.edit(
            f"📂 **كتب قسم ({cat_name}):**\n\nاضغط على الكتاب لتنزيله فوراً:",
            buttons=book_buttons
        )
        return
        
    if data.startswith('book_'):
        book_prefix = data.replace('book_', '')
        target_file = None
        target_path = None
        
        for cat_info in CATEGORIES.values():
            cat_path = os.path.join(BASE_DIR, cat_info["name"])
            if os.path.exists(cat_path):
                for f in os.listdir(cat_path):
                    if f.startswith(book_prefix):
                        target_file = f
                        target_path = cat_path
                        break
            if target_file:
                break
                
        if target_file:
            file_path = os.path.join(target_path, target_file)
            await event.answer("جاري إرسال الكتاب...")
            await event.respond(f"📖 تفضل كتاب: **{target_file.replace('_', ' ').replace('.pdf', '')}**")
            await client.send_file(event.chat_id, file_path)
        else:
            await event.answer("عذراً، لم يتم العثور على الكتاب.", alert=True)

@client.on(events.NewMessage(func=lambda e: e.is_private and not e.text.startswith('/')))
async def handle_user_input(event):
    text = event.text.strip()
    all_files = []
    for cat_info in CATEGORIES.values():
        cat_path = os.path.join(BASE_DIR, cat_info["name"])
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
