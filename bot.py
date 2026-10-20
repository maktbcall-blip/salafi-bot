import os
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8842393887:AAGnUuwXSwDE7pUP_Ohgw7oolf87BCCjoV0")

ADMIN_ID = int(os.environ.get("ADMIN_ID", 8779419591))
CHANNEL_USERNAME = '@Alsalafi200'

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# الأقسام الرئيسية الـ 12
CATEGORIES = {
    "c1": {"name": "القرآن الكريم وعلومه", "keywords": ["قرآن", "تفسير", "مصحف", "تجويد", "إعجاز", "السيوطي"]},
    "c2": {"name": "التوحيد والعقيدة", "keywords": ["توحيد", "عقيدة", "الواسطية", "الحموية", "ابن باز", "عثيمين", "تيمية"]},
    "c3": {"name": "الفقه وأصوله", "keywords": ["فقه", "أصول", "أحكام", "صلاة", "صيام", "حج", "الفوزان"]},
    "c4": {"name": "الحديث وعلومه", "keywords": ["حديث", "سنن", "صحيح", "مسند", "النووي", "الأربعين"]},
    "c5": {"name": "السيرة والتاريخ الإسلامي", "keywords": ["سيرة", "تاريخ", "الغزوات", "الخلافة", "ابن هشام"]},
    "c6": {"name": "الآداب والأخلاق والرقائق والأدعية والأذكار", "keywords": ["أذكار", "آداب", "رقائق", "أخلاق", "دعاء", "الوابل الصيب"]},
    "c7": {"name": "محاربة البدع والردود", "keywords": ["بدع", "بدعة", "ردود", "الرد", "تحذير"]},
    "c8": {"name": "الفرق الضالة والمبتدعة", "keywords": ["فرق", "ضالة", "خوارج", "رافضة", "صوفية"]},
    "c9": {"name": "محاربة الإلحاد", "keywords": ["إلحاد", "ملحدين", "شبهات"]},
    "c10": {"name": "الرد على الشبهات", "keywords": ["شبهات", "شبهة", "الردود العلمية"]},
    "c11": {"name": "فوائد ونصائح متنوعة", "keywords": ["فوائد", "نصائح", "متنوعة", "رسائل", "طالب العلم"]},
    "c12": {"name": "السير والتراجم", "keywords": ["تراجم", "ترجمة", "سير", "أعلام", "العلماء", "وفيات"]}
}

BASE_DIR = "library_books"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

for cat_info in CATEGORIES.values():
    cat_dir = os.path.join(BASE_DIR, cat_info["name"])
    if not os.path.exists(cat_dir):
        os.makedirs(cat_dir)

async def check_subscription(user_id):
    if user_id == ADMIN_ID:
        return True
    try:
        await client(GetParticipantRequest(channel=CHANNEL_USERNAME, participant=user_id))
        return True
    except UserNotParticipantError:
        return False
    except Exception:
        return True

def get_sections_keyboard():
    buttons = []
    for key, cat_info in CATEGORIES.items():
        name = cat_info["name"]
        cat_path = os.path.join(BASE_DIR, name)
        total_count = 0
        if os.path.exists(cat_path):
            for root, dirs, files in os.walk(cat_path):
                total_count += len(files)
        btn_text = f"{name} ({total_count})"
        buttons.append([Button.inline(btn_text, data=f"cat_{key}".encode('utf-8'))])
    return buttons

def get_sub_keyboard():
    return [
        [Button.url("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [Button.inline("🔄 تحقق من الاشتراك", data=b"check_sub")]
    ]

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    if not await check_subscription(user_id):
        await event.respond(
            "⚠️ **عذراً، يجب عليك الاشتراك في قناة المكتبة أولاً لتتمكن من استخدام البوت واستعراض الكتب!**\n\n"
            f"قناة البوت: {CHANNEL_USERNAME}\n\n"
            "بعد الاشتراك، اضغط على زر (تحقق من الاشتراك) بالأسفل 👇",
            buttons=get_sub_keyboard()
        )
        return

    await event.respond(
        "مرحباً بك في بوت المكتبة السلفية المرتبة 📚\n\n"
        "اختر القسم الرئيسي من الأزرار بالأسفل:",
        buttons=get_sections_keyboard()
    )

# دالة رفع وتصنيف الكتاب بإنشاء مجلد المؤلف تلقائياً إذا لم يكن موجوداً
@client.on(events.NewMessage(func=lambda e: e.is_private and e.sender_id == ADMIN_ID and e.document))
async def save_new_book(event):
    try:
        temp_path = await event.download_media(file=BASE_DIR)
        file_name = os.path.basename(temp_path)
        file_lower = file_name.lower()
        
        # 1. تحديد القسم الرئيسي المناسب بناءً على الكلمات المفتاحية
        target_cat_name = "فوائد ونصائح متنوعة"
        for cat_info in CATEGORIES.values():
            for kw in cat_info["keywords"]:
                if kw.lower() in file_lower:
                    target_cat_name = cat_info["name"]
                    break
            if target_cat_name != "فوائد ونصائح متنوعة":
                break
                
        # 2. استخراج اسم المؤلف تلقائياً من اسم الملف (مثال: البحث عن الكلمات بعد كلمة "لإمام" أو "للشيخ" أو "للباحث" أو استخدام اسم افتراضي)
        author_name = "مؤلفات متنوعة"
        if "للإمام" in file_name:
            parts = file_name.split("للإمام")
            if len(parts) > 1:
                author_name = "الإمام " + parts[1].replace("_", " ").replace(".pdf", "").strip().split()[0]
        elif "للعلامة" in file_name:
            parts = file_name.split("للعلامة")
            if len(parts) > 1:
                author_name = "العلامة " + parts[1].replace("_", " ").replace(".pdf", "").strip().split()[0]
        elif "للشيخ" in file_name:
            parts = file_name.split("للشيخ")
            if len(parts) > 1:
                author_name = "الشيخ " + parts[1].replace("_", " ").replace(".pdf", "").strip().split()[0]
        elif "لابن" in file_name:
            parts = file_name.split("لابن")
            if len(parts) > 1:
                author_name = "ابن " + parts[1].replace("_", " ").replace(".pdf", "").strip().split()[0]
        else:
            # محاولة أخذ آخر الكلمات من اسم الملف كاسم مؤلف
            clean_clean = file_name.replace(".pdf", "").replace("_", " ")
            author_name = clean_clean.split()[-1] if len(clean_clean.split()) > 0 else "مؤلفون آخرون"

        # تنظيف اسم المؤلف
        author_name = author_name.strip()
        
        # 3. إنشاء مسار القسم والمؤلف تلقائياً (ديناميكي)
        target_dir = os.path.join(BASE_DIR, target_cat_name, author_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir) # إنشاء مجلد جديد للمؤلف تلقائياً فوراً!
            
        final_path = os.path.join(target_dir, file_name)
        if os.path.exists(temp_path) and temp_path != final_path:
            if os.path.exists(final_path):
                os.remove(final_path)
            os.rename(temp_path, final_path)
            
        await event.respond(f"✅ تم إنشاء قسم خاص وتصنيف الكتاب تلقائياً في:\n📂 **{target_cat_name}** ⬅️ **{author_name}**\n\n📄 باسم: `{file_name}`")
    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء التصنيف: {str(e)}")

@client.on(events.CallbackQuery)
async def callback_handler(event):
    await event.answer()
    user_id = event.sender_id
    data = event.data.decode('utf-8')
    
    if data == 'check_sub':
        if await check_subscription(user_id):
            await event.edit("✅ **شكراً لاشتراكك! اختر القسم الرئيسي:**", buttons=get_sections_keyboard())
        else:
            await event.answer("❌ لم تقم بالاشتراك بعد!", alert=True)
        return

    if not await check_subscription(user_id):
        await event.edit("⚠️ **عذراً، يجب عليك الاشتراك في القناة أولاً!**", buttons=get_sub_keyboard())
        return
    
    if data == 'home':
        await event.edit("مرحباً بك في بوت المكتبة السلفية 📚\n\nاختر القسم الرئيسي:", buttons=get_sections_keyboard())
        return
        
    # عرض المؤلفين الموجودين داخل القسم ديناميكياً
    if data.startswith('cat_'):
        cat_key = data.replace('cat_', '')
        cat_info = CATEGORIES.get(cat_key)
        if not cat_info:
            return
            
        cat_path = os.path.join(BASE_DIR, cat_info["name"])
        sub_authors = []
        if os.path.exists(cat_path):
            sub_authors = [d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))]
            
        author_buttons = []
        for author in sub_authors:
            author_path = os.path.join(cat_path, author)
            count = len(os.listdir(author_path)) if os.path.exists(author_path) else 0
            btn_text = f"👤 {author} ({count})"
            author_buttons.append([Button.inline(btn_text, data=f"aut_{cat_key}_{author}".encode('utf-8'))])
            
        author_buttons.append([Button.inline("⬅️ عودة للأقسام الرئيسية", data='home')])
        
        await event.edit(f"📂 **قسم ({cat_info['name']}):**\n\nاختر المؤلف المطلوب:", buttons=author_buttons)
        return
        
    # عرض الكتب الخاصة بالمؤلف
    if data.startswith('aut_'):
        parts = data.split('_', 2)
        cat_key = parts[1]
        author_name = parts[2]
        
        cat_info = CATEGORIES.get(cat_key)
        if not cat_info:
            return
            
        author_path = os.path.join(BASE_DIR, cat_info["name"], author_name)
        files = sorted(os.listdir(author_path)) if os.path.exists(author_path) else []
        
        if not files:
            await event.edit(
                f"📁 قسم **{author_name}** فارغ حالياً.",
                buttons=[[Button.inline("⬅️ عودة للأقسام", data=f"cat_{cat_key}")]]
            )
            return
            
        book_buttons = []
        for idx, file in enumerate(files):
            clean_name = file.replace("_", " ").replace('.pdf', '')
            book_buttons.append([Button.inline(f"📖 {clean_name}", data=f"get_{cat_key}_{author_name}_{idx}".encode('utf-8'))])
            
        book_buttons.append([Button.inline("⬅️ عودة للمؤلفين", data=f"cat_{cat_key}")])
        
        await event.edit(f"📚 **{author_name}:**\n\nاضغط على الكتاب لتنزيله فوراً:", buttons=book_buttons)
        return
        
    # تنزيل وإرسال الكتاب
    if data.startswith('get_'):
        parts = data.split('_', 2)
        cat_key = parts[1]
        remaining = parts[2]
        # استخراج الفهرس الأخير واسم المؤلف بدقة
        last_underscore_idx = remaining.rfind('_')
        author_name = remaining[:last_underscore_idx]
        book_index = int(remaining[last_underscore_idx+1:])
        
        cat_info = CATEGORIES.get(cat_key)
        if not cat_info:
            return
            
        author_path = os.path.join(BASE_DIR, cat_info["name"], author_name)
        files = sorted(os.listdir(author_path)) if os.path.exists(author_path) else []
        
        if 0 <= book_index < len(files):
            target_file = files[book_index]
            file_path = os.path.join(author_path, target_file)
            await event.respond(f"📖 تفضل كتاب: **{target_file.replace('_', ' ').replace('.pdf', '')}**")
            await client.send_file(event.chat_id, file_path)
        else:
            await event.answer("عذراً، لم يتم العثور على الكتاب.", alert=True)

print("Bot is running...")
client.run_until_disconnected()
