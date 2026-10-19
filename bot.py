import logging
from telethon import Button, TelegramClient, events

# بياناتك الصحيحة والتنصيصات سليمة
API_ID = 32863080
API_HASH = "56761d4c8f04011adf5779ca13095184"
BOT_TOKEN = "8842393887:AAFqtGCAc6ybVYgQDarwNkLe5nrSN9lgnHY"

# الآيدي الخاص بك (مدير المكتبة الوحيد)
ADMIN_ID = 8779419591

logging.basicConfig(level=logging.INFO)

# إنشاء العميل الخاص بالبوت
client = TelegramClient("alsalafe_session_v3", API_ID, API_HASH).start(
    bot_token=BOT_TOKEN
)

BOOKS_DATABASE = {}


@client.on(events.NewMessage(pattern="/start"))
async def cmd_start(event):
  keyboard = [
      [Button.inline("📚 تصفح الكتب", data=b"list_books")],
      [Button.inline("🔍 بحث عن كتاب", data=b"search_prompt")],
  ]
  await event.respond(
      "مرحباً بك في بوت **مكتبة السلفي**! 📖\nاختر ما تحب من الخيارات أدناه:",
      buttons=keyboard,
  )


@client.on(events.CallbackQuery(data=b"list_books"))
async def list_books(event):
  if not BOOKS_DATABASE:
    await event.answer("عذراً، مكتبة السلفي فارغة حالياً.", alert=True)
    return

  keyboard = []
  for book_name in BOOKS_DATABASE.keys():
    keyboard.append([Button.inline(book_name, data=f"get_{book_name}".encode())])

  keyboard.append([Button.inline("🔙 القائمة الرئيسية", data=b"main_menu")])

  await event.edit(
      "إليك الكتب المتوفرة في مكتبة السلفي:", buttons=keyboard
  )


@client.on(events.CallbackQuery(data=b"main_menu"))
async def main_menu(event):
  keyboard = [
      [Button.inline("📚 تصفح الكتب", data=b"list_books")],
      [Button.inline("🔍 بحث عن كتاب", data=b"search_prompt")],
  ]
  await event.edit(
      "مرحباً بك في بوت **مكتبة السلفي**! 📖\nاختر ما تحب من الخيارات أدناه:",
      buttons=keyboard,
  )


@client.on(events.CallbackQuery(pattern=b"get_"))
async def send_book(event):
  data_bytes = event.data
  book_name = data_bytes.decode("utf-8").replace("get_", "")
  message_obj = BOOKS_DATABASE.get(book_name)

  if message_obj:
    await event.respond(message_obj)
    await event.answer("إليك الكتاب يا فاعل الخير 📚")
  else:
    await event.answer("عذراً، لم يتم العثور على هذا الكتاب.", alert=True)


@client.on(events.CallbackQuery(data=b"search_prompt"))
async def search_prompt(event):
  await event.answer(
      "خاصية البحث المباشر قيد التطوير، يمكنك حالياً تصفح الكتب عبر زر"
      " (تصفح الكتب).",
      alert=True,
  )


# 4. إضافة كتاب للمكتبة (حصرية للمشرف فقط)
@client.on(events.NewMessage(pattern=r"/add (.+)"))
async def add_book(event):
  # التحقق من أن المرسل هو أنت حصراً
  if event.sender_id != ADMIN_ID:
    await event.respond(
        "عذراً! إضافة الكتب مخصصة لمدير المكتبة فقط 🚫"
    )
    return

  book_name = event.pattern_match.group(1).strip()

  if event.message.media:
    BOOKS_DATABASE[book_name] = event.message
    await event.respond(
        f"تم بنجاح إضافة كتاب: **{book_name}** إلى مكتبة السلفي! 🎉"
    )
  else:
    await event.respond(
        "الرجاء إرفاق ملف الكتاب (PDF) مع أمر الإضافة هكذا:\n`/add اسم"
        " الكتاب` مع الملف."
    )


print("بوت مكتبة السلفي يعمل الآن بصلاحيات المدير الكاملة...")
client.run_until_disconnected()
