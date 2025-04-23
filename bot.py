import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FAQ, BOT_ID, BOT_HASH

# Базовое логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=f"{BOT_ID}:{BOT_HASH}")
dp = Dispatcher()

# Клавиатура 
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=q, callback_data=f"faq_{i}")]
        for i, q in enumerate(FAQ.keys())
    ])
    return keyboard

# Обработчик команды /start(bruh)
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        'Здравствуйте! Я бот-консультант по 1С:Предприятие. Выберите интересующий вас вопрос:',
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    help_text = """
    Доступные команды:
    /start - Начать работу с ботом
    /help - Показать это сообщение
    /faq - Часто задаваемые вопросы
    """
    await message.answer(help_text)

# Обработчик тыканья на кнопки
@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    if callback.data.startswith("faq_"):
        index = int(callback.data.split("_")[1])
        question = list(FAQ.keys())[index]
        answer = FAQ[question]
        await callback.message.edit_text(
            f"Вопрос: {question}\n\nОтвет: {answer}",
            reply_markup=get_main_keyboard()
        )
    elif callback.data == "support":
        await callback.message.edit_text(
            "Для связи с технической поддержкой напишите ваш вопрос, "
            "и наш специалист ответит вам в ближайшее время."
        )
    elif callback.data == "back_to_start":
        await callback.message.edit_text(
            'Чем могу помочь?',
            reply_markup=get_main_keyboard()
        )

# Обработчик  сообщений
@dp.message()
async def handle_message(message: types.Message):
    message_text = message.text.lower()
    for question, answer in FAQ.items():
        if question.lower() in message_text:
            await message.answer(answer)
            return
    await message.answer(
        "Извините, я не нашел ответа на ваш вопрос. "
        "Попробуйте переформулировать или обратитесь к специалисту поддержки."
    )

# Запуск 
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 