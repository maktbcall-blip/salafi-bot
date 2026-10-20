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

# الأقسام الـ 12 الرئيسية مع المؤلفين والشروحات التابعة لها
CATEGORIES = {
    "cat_1": {
        "name": "القرآن الكريم وعلومه",
        "authors": {
            "ibn_katheer_quran": {"name": "تفسير ابن كثير ومصنفات القرآن", "keywords": ["تفسير ابن كثير", "قرآن", "مصحف", "تجويد", "قراءات"]}
        }
    },
    "cat_2": {
        "name": "التوحيد والعقيدة",
        "authors": {
            "ibn_taymiyyah": {"name": "مؤلفات شيخ الإسلام ابن تيمية", "keywords": ["تيمية", "الواسطية", "الحموية", "التدميرية"]},
            "ibn_taymiyyah_sharh": {"name": "شروحات كتب ابن تيمية", "keywords": ["شرح الواسطية", "شرح الحموية"]},
            "ibn_othaymeen_aqidah": {"name": "مؤلفات وشروحات ابن عثيمين في العقيدة", "keywords": ["عثيمين", "القواعد المثلى", "فتح رب البرية"]}
        }
    },
    "cat_3": {
        "name": "الفقه وأصوله",
        "authors": {
            "ibn_othaymeen_fiqh": {"name": "مؤلفات الشيخ ابن عثيمين في الفقه", "keywords": ["الشرح الممتع", "الممتع", "مجموع فتاوى ابن عثيمين"]},
            "ibn_othaymeen_sharh": {"name": "شروحات فقهية للشيخ ابن عثيمين", "keywords": ["شرح بلوغ المرام", "شرح زاد المستقنع"]},
            "fawzan_fiqh": {"name": "مؤلفات وشروحات الشيخ صالح الفوزان", "keywords": ["الفوزان", "الملخص الفقهي"]}
        }
    },
    "cat_4": {
        "name": "الحديث وعلومه",
        "authors": {
            "nawawi": {"name": "الإمام النووي (الأربعين وغيرها)", "keywords": ["النووي", "الأربعين", "رياض الصالحين"]},
            "nawawi_sharh": {"name": "شروحات كتب الإمام النووي", "keywords": ["شرح الأربعين", "شرح رياض الصالحين", "بهجة الناظرين"]}
        }
    },
    "cat_5": {
        "name": "السيرة والتاريخ الإسلامي",
        "authors": {
            "ibn_hisham_sira": {"name": "كتب السيرة النبوية والتاريخ", "keywords": ["سيرة", "ابن هشام", "تاريخ", "الغزوات", "الخلافة"]}
        }
    },
    "cat_6": {
        "name": "الآداب والأخلاق والرقائق والأدعية والأذكار",
        "authors": {
            "adhkar_books": {"name": "كتب الأذكار والرقاق والآداب", "keywords": ["أذكار", "آداب", "رقائق", "رقاق", "أخلاق", "دعاء"]}
        }
    },
    "cat_7": {
        "name": "محاربة البدع والردود",
        "authors": {
            "bida_books": {"name": "كتب التحذير من البدع والردود", "keywords": ["بدع", "بدعة", "ردود", "الرد", "تحذير"]}
        }
    },
    "cat_8": {
        "name": "الفرق الضالة والمبتدعة",
        "authors": {
            "firaq_books": {"name": "كتب دراسة الفرق والرد عليها", "keywords": ["فرق", "ضالة", "خوارج", "رافضة", "صوفية", "اشاعرة"]}
        }
    },
    "cat_9": {
        "name": "محاربة الإلحاد",
        "authors": {
            "atheism_books": {"name": "كتب الرد على الإلحاد والشبهات المادية", "keywords": ["إلحاد", "ملحدين", "العلم والدين"]}
        }
    },
    "cat_10": {
        "name": "الرد على الشبهات",
        "authors": {
            "shubuhat_books": {"name": "كتب دفع الشبهات والردود العلمية", "keywords": ["شبهات", "شبهة", "الردود العلمية"]}
        }
    },
    "cat_11": {
        "name": "فوائد ونصائح متنوعة",
        "authors": {
            "fawaid_books": {"name": "الفوائد والنصائح والرسائل المتنوعة", "keywords": ["فوائد", "نصائح", "متنوعة", "رسائل", "مفيدة", "طالب", "العلم"]}
        }
    },
    "cat_12": {
        "name": "السير والتراجم",
        "authors": {
            "tarajim_books": {"name": "كتب التراجم وأعلام العلماء والوفيات", "keywords": ["تراجم", "ترجمة", "سير", "أعلام", "العلماء", "وفيات"]}
        }
    }
}

BASE_DIR = "library_books"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# إنشاء المجلدات هرمياً لكل الأقسام
for cat_key, cat_info in CATEGORIES.items():
    cat_dir = os.path.join(BASE_DIR, cat_info["name"])
    for auth_key, auth_info in cat_info["authors"].items():
        auth_dir = os.path.join(cat_dir, auth_info["name"])
        if not os.path.exists(auth_dir):
            os.makedirs(auth_dir)

# دالة التحقق من الاشتراك
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
        buttons.append([Button.inline(btn_text, data=f"maincat_{key}".encode('utf-8'))])
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
        
        matched_cat_name = CATEGORIES["cat_2"]["name"]
        matched_auth_key = list(CATEGORIES["cat_2"]["authors"].keys())[0]
        matched_auth_name = CATEGORIES["cat_2"]["authors"][matched_auth_key]["name"]
        
        found = False
        for cat_key, cat_info in CATEGORIES.items():
            for auth_key, auth_info in cat_info["authors"].items():
                for kw in auth_info["keywords"]:
                    if kw in file_lower:
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
    
    if data == 'back_to_home':
        await event.edit("مرحباً بك في بوت المكتبة السلفية 📚\n\nاختر القسم الرئيسي:", buttons=get_sections_keyboard())
        return
        
    if data.startswith('maincat_'):
        cat_key = data.replace('maincat_', '')
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
            author_buttons.append([Button.inline(btn_text, data=f"auth_{cat_key}_{auth_key}".encode('utf-8'))])
            
        author_buttons.append([Button.inline("⬅️ عودة للأقسام الرئيسية", data='back_to_home')])
        
        await event.edit(f"📂 **قسم ({cat_info['name']}):**\n\nاختر المؤلف أو قسم الشروحات المطلوب:", buttons=author_buttons)
        return
        
    if data.startswith('auth_'):
        parts = data.split('_', 2)
        cat_key = parts[1]
        auth_key = parts[2]
        
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
                buttons=[[Button.inline("⬅️ عودة للأقسام", data=f"maincat_{cat_key}")]]
            )
            return
            
        book_buttons = []
        for idx, (file, path) in enumerate(files):
            clean_name = file.replace("_", " ").replace('.pdf', '')
            book_buttons.append([Button.inline(f"📖 {clean_name}", data=f"getbook_{cat_key}_{auth_key}_{idx}".encode('utf-8'))])
            
        book_buttons.append([Button.inline("⬅️ عودة للمؤلفين", data=f"maincat_{cat_key}")])
        
        await event.edit(f"📚 **{auth_info['name']}:**\n\nاضغط على الكتاب لتنزيله فوراً:", buttons=book_buttons)
        return
        
    if data.startswith('getbook_'):
        parts = data.split('_')
        cat_key = f"{parts[1]}_{parts[2]}"
        auth_key = parts[3]
        book_index = int(parts[4])
        
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
