from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os
from config import TOKEN, CHAT_ID  # Берём данные из конфига

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Обычная клавиатура (только в ЛС)
private_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
private_keyboard.add(KeyboardButton("🏴‍☠️ Наши ссылки"))

# Inline-клавиатура (онлайн-кнопки)
inline_kb = InlineKeyboardMarkup(row_width=1)
inline_kb.add(
    InlineKeyboardButton("💬 Наш чат", callback_data="get_chat_link"),
    InlineKeyboardButton("⚡ Экспресс Бот", url="https://t.me/ExpressBot")
)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.chat.type == "private":  # В ЛС показываем клавиатуру
        await message.answer("Привет! Здесь ты можешь получить ссылки.", reply_markup=private_keyboard)
    else:
        await message.answer("Этот бот работает в ЛС и в группе.")

@dp.message_handler(lambda message: message.text.lower() in ["ссылка", "/links"])
async def send_links(message: types.Message):
    if message.chat.type == "private":  # В ЛС с inline-клавиатурой
        await message.answer_photo(
            photo="https://telegra.ph/file/your-image.jpg",
            caption="Выбери нужный вариант:",
            reply_markup=inline_kb
        )
    else:  # В группе без клавиатуры
        await message.answer_photo(
            photo="https://telegra.ph/file/your-image.jpg",
            caption="Вот ссылка на наш чат:\n💬 t.me/joinchat/yourchat"
        )

@dp.callback_query_handler(lambda call: call.data == "get_chat_link")
async def generate_link(call: types.CallbackQuery):
    invite_link = await bot.export_chat_invite_link(CHAT_ID)  # Генерация ссылки на чат
    await call.message.answer(f"💬 Чат: {invite_link}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
