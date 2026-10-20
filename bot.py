import os
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

# بيانات التوثيق
API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8842393887:AAGnUuwXSwDE7pUP_Ohgw7oolf87BCCjoV0")

# الآيدي الشخصي للمشرف ومعرف القناة للاشتراك الإجباري
ADMIN_ID = int(os.environ.get("ADMIN_ID", 8779419591))
CHANNEL_USERNAME = '@Alsalafi200'

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# الأقسام مع هيكل المؤلفين بمفاتيح مختصرة وثابتة
CATEGORIES = {
    "c1": {
        "name": "القرآن الكريم وعلومه",
        "authors": {
            "a1": {"name": "تفسير ابن كثير ومصنفات القرآن", "keywords": ["ابن كثير", "تفسير القرآن", "مصحف", "تجويد"]}
        }
    },
    "c2": {
        "name": "التوحيد والعقيدة",
        "authors": {
            "a2_1": {"name": "مؤلفات وشروحات الإمام ابن باز", "keywords": ["ابن_باز", "عبدالعزيز_بن_باز", "الشيخ_عبدالعزيز", "تعليق ابن باز"]},
            "a2_2": {"name": "مؤلفات وشروحات ابن عثيمين في العقيدة", "keywords": ["ابن عثيمين", "العثيمين", "القواعد المثلى", "فتح رب البرية"]},
            "a2_3": {"name": "مؤلفات شيخ الإسلام ابن تيمية", "keywords": ["ابن تيمية", "شيخ الإسلام", "الواسطية", "الحموية"]},
            "a2_4": {"name": "شروحات كتب ابن تيمية", "keywords": ["شرح الواسطية", "شرح الحموية"]}
        }
    },
    "c3": {
        "name": "الفقه وأصوله",
        "authors": {
            "a3_1": {"name": "مؤلفات الشيخ ابن عثيمين في الفقه", "keywords": ["ابن عثيمين", "العثيمين", "الشرح الممتع"]},
            "a3_2": {"name": "مؤلفات وشروحات الشيخ صالح الفوزان", "keywords": ["الفوزان", "الملخص الفقهي"]}
        }
    },
    "c4": {
        "name": "الحديث وعلومه",
        "authors": {
            "a4_1": {"name": "الإمام النووي (الأربعين وغيرها)", "keywords": ["النووي", "الأربعين", "رياض الصالحين"]},
            "a4_2": {"name": "شروحات كتب الإمام النووي", "keywords": ["شرح الأربعين", "شرح رياض الصالحين"]}
        }
    },
    "c5": {
        "name": "السيرة والتاريخ الإسلامي",
        "authors": {
            "a5_1": {"name": "كتب السيرة النبوية والتاريخ", "keywords": ["سيرة", "ابن هشام", "تاريخ", "الغزوات"]}
        }
    },
    "c6": {
        "name": "الآداب والأخلاق والرقائق والأدعية والأذكار",
        "authors": {
            "a6_1": {"name": "كتب الأذكار والرقاق والآداب", "keywords": ["أذكار", "آداب", "رقائق", "أخلاق", "دعاء", "الوابل الصيب"]}
        }
    },
    "c7": {
        "name": "محاربة البدع والردود",
        "authors": {
            "a7_1": {"name": "كتب التحذير من البدع والردود", "keywords": ["بدع", "بدعة", "ردود", "الرد"]}
        }
    },
    "c8": {
        "name": "الفرق الضالة والمبتدعة",
        "authors": {
            "a8_1": {"name": "كتب دراسة الفرق والرد عليها", "keywords": ["فرق", "ضالة", "خوارج", "رافضة", "صوفية"]}
        }
    },
    "c9": {
        "name": "محاربة الإلحاد",
        "authors": {
            "a9_1": {"name": "كتب الرد على الإلحاد والشبهات", "keywords": ["إلحاد", "ملحدين", "العلم والدين"]}
        }
    },
    "c10": {
        "name": "الرد على الشبهات",
        "authors": {
            "a10_1": {"name": "كتب دفع الشبهات والردود العلمية", "keywords": ["شبهات", "شبهة", "الردود العلمية"]}
        }
    },
    "c11": {
        "name": "فوائد ونصائح متنوعة",
        "authors": {
            "a11_1": {"name": "الفوائد والنصائح والرسائل المتنوعة", "keywords": ["فوائد", "نصائح", "متنوعة", "رسائل", "طالب العلم"]}
        }
    },
    "c12": {
        "name": "السير والتراجم",
        "authors": {
            "a12_1": {"name": "كتب التراجم وأعلام العلماء والوفيات", "keywords": ["تراجم", "ترجمة", "سير", "أعلام", "وفيات"]}
        }
    }
}

BASE_DIR = "library_books"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

for cat_key, cat_info in CATEGORIES.items():
    cat_dir = os.path.join(BASE_DIR, cat_info["name"])
    for auth_key, auth_info in cat_info["authors"].items():
        auth_dir = os.path.join(cat_dir, auth_info["name"])
        if not os.path.exists(auth_dir):
            os.makedirs(auth_dir)

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

@client.on(events.NewMessage(func=lambda e: e.is_private and e.sender_id == ADMIN_ID and e.document))
async def save_new_book(event):
    try:
        temp_path = await event.download_media(file=BASE_DIR)
        file_name = os.path.basename(temp_path)
        file_lower = file_name.lower()
        
        matched_cat_name = CATEGORIES["c2"]["name"]
        matched_auth_name = CATEGORIES["c2"]["authors"]["a2_1"]["name"]
        
        found = False
        for cat_key, cat_info in CATEGORIES.items():
            for auth_key, auth_info in cat_info["authors"].items():
                for kw in auth_info["keywords"]:
                    if kw.lower() in file_lower:
                        matched_cat_name = cat_info["name"]
                        matched_auth_name = auth_info["name"]
                        found = True
                        break
                if found:
                    break
            if found:
                break
                
        target_dir = os.path.join(BASE_DIR, matched_cat_name, matched_auth_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        final_path = os.path.join(target_dir, file_name)
        if os.path.exists(temp_path) and temp_path != final_path:
            if os.path.exists(final_path):
                os.remove(final_path)
            os.rename(temp_path, final_path)
            
        await event.respond(f"✅ تم تصنيف وحفظ الكتاب تلقائياً في:\n📂 **{matched_cat_name}** ⬅️ **{matched_auth_name}**\n\n📄 باسم: `{file_name}`")
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
        
    # عرض المؤلفين للقسم الرئيسي (مثال: cat_c2)
    if data.startswith('cat_'):
        cat_key = data.replace('cat_', '')
        cat_info = CATEGORIES.get(cat_key)
        if not cat_info:
            return
            
        author_buttons = []
        for auth_key, auth_info in cat_info["authors"].items():
            auth_path = os.path.join(BASE_DIR, cat_info["name"], auth_info["name"])
            count = 0
            if os.path.exists(auth_path):
                for root, dirs, files in os.walk(auth_path):
                    count += len(files)
            btn_text = f"👤 {auth_info['name']} ({count})"
            # تمرير مفتاح القسم ومفتاح المؤلف بشكل مختصر جداً وامن
            author_buttons.append([Button.inline(btn_text, data=f"aut_{cat_key}_{auth_key}".encode('utf-8'))])
            
        author_buttons.append([Button.inline("⬅️ عودة للأقسام الرئيسية", data='home')])
        
        await event.edit(f"📂 **قسم ({cat_info['name']}):**\n\nاختر المؤلف أو قسم الشروحات المطلوب:", buttons=author_buttons)
        return
        
    # عرض الكتب الخاصة بمؤلف معين (مثال: aut_c2_a2_1)
    if data.startswith('aut_'):
        parts = data.split('_')
        cat_key = parts[1]
        auth_key = "_".join(parts[2:]) # استخلاص مفتاح المؤلف بدقة
        
        cat_info = CATEGORIES.get(cat_key)
        if not cat_info or auth_key not in cat_info["authors"]:
            return
            
        auth_info = cat_info["authors"][auth_key]
        auth_path = os.path.join(BASE_DIR, cat_info["name"], auth_info["name"])
        
        files = []
        if os.path.exists(auth_path):
            for root, dirs, filenames in os.walk(auth_path):
                for f in filenames:
                    files.append((f, auth_path))
                    
        if not files:
            await event.edit(
                f"📁 قسم **{auth_info['name']}** فارغ حالياً.",
                buttons=[[Button.inline("⬅️ عودة للأقسام", data=f"cat_{cat_key}")]]
            )
            return
            
        book_buttons = []
        for idx, (file, path) in enumerate(files):
            clean_name = file.replace("_", " ").replace('.pdf', '')
            # زر تحميل الكتاب مع تمرير المفاتيح والفهرس
            book_buttons.append([Button.inline(f"📖 {clean_name}", data=f"get_{cat_key}_{auth_key}_{idx}".encode('utf-8'))])
            
        book_buttons.append([Button.inline("⬅️ عودة للمؤلفين", data=f"cat_{cat_key}")])
        
        await event.edit(f"📚 **{auth_info['name']}:**\n\nاضغط على الكتاب لتنزيله فوراً:", buttons=book_buttons)
        return
        
    # تنزيل وإرسال الكتاب للمستخدم
    if data.startswith('get_'):
        parts = data.split('_')
        cat_key = parts[1]
        auth_key = "_".join(parts[2:-1])
        book_index = int(parts[-1])
        
        cat_info = CATEGORIES.get(cat_key)
        if not cat_info or auth_key not in cat_info["authors"]:
            return
            
        auth_info = cat_info["authors"][auth_key]
        auth_path = os.path.join(BASE_DIR, cat_info["name"], auth_info["name"])
        
        files = []
        if os.path.exists(auth_path):
            for root, dirs, filenames in os.walk(auth_path):
                for f in filenames:
                    files.append((f, auth_path))
                    
        if 0 <= book_index < len(files):
            target_file, target_path = files[book_index]
            file_path = os.path.join(target_path, target_file)
            await event.respond(f"📖 تفضل كتاب: **{target_file.replace('_', ' ').replace('.pdf', '')}**")
            await client.send_file(event.chat_id, file_path)
        else:
            await event.answer("عذراً، لم يتم العثور على الكتاب.", alert=True)

print("Bot is running...")
client.run_until_disconnected()
