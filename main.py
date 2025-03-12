import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile
import time

from config import TOKEN, CHAT_ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Храним активные ссылки, чтобы не выдавать новые раньше времени
active_links = {}

# Функция генерации ссылки на чат
async def create_invite_link():
    chat = await bot.get_chat(CHAT_ID)
    invite_link = await chat.create_invite_link(expire_date=int(time.time()) + 900, member_limit=2)
    return invite_link.invite_link

# Клавиатура для инлайн-кнопок
def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Наш чат", callback_data="get_chat_link")],
        [InlineKeyboardButton(text="⚡ Экспресс Бот", url="https://t.me/FastShopkz_bot")]
    ])
    return keyboard

# Обычная клавиатура
def get_reply_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="🏴‍☠️ Наши ссылки")
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    # Отправка картинки
    photo = FSInputFile("welcome.jpg")  # Убедись, что этот файл есть в проекте
    text = "🎉 Добро пожаловать!\n\n🔍 На связи лучший сервис по поиску органики.\n⏳ Ссылка действует 15 минут и доступна только 2 людям.\n📩 Для получения новой ссылки нажмите соответствующую кнопку!"

    await message.answer_photo(photo=photo, caption=text, reply_markup=get_inline_keyboard())

# Обработчик кнопки "Наши ссылки"
@dp.message()
async def handle_links_button(message: types.Message):
    if message.text == "🏴‍☠️ Наши ссылки":
        user_id = message.from_user.id

        if user_id in active_links:
            remaining_time = int(active_links[user_id] - time.time())
            if remaining_time > 0:
                await message.answer(f"⚠️ У вас уже есть активная ссылка!\n⏳ Новую можно получить через {remaining_time // 60} мин {remaining_time % 60} сек.")
                return

        invite_link = await create_invite_link()
        active_links[user_id] = time.time() + 900  # Запоминаем время истечения ссылки

        await message.answer(f"👉 Ваша ссылка: {invite_link}")

# Обработчик инлайн-кнопки "Наш чат"
@dp.callback_query(lambda c: c.data == "get_chat_link")
async def send_chat_link(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in active_links:
        remaining_time = int(active_links[user_id] - time.time())
        if remaining_time > 0:
            await callback.message.answer(f"⚠️ У вас уже есть активная ссылка!\n⏳ Новую можно получить через {remaining_time // 60} мин {remaining_time % 60} сек.")
            return

    invite_link = await create_invite_link()
    active_links[user_id] = time.time() + 900

    await callback.message.answer(f"👉 Ваша ссылка: {invite_link}")
    await callback.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
