from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from tgbot.keyboards.inline import langugage_keyboard



async def user_start(message: Message):
    await message.answer(
        "Botga xush kelibsiz\n\nДобро пожаловать в бот"
    )
    await message.answer("Foydalanish tilini tanlang\n\nВыберите язык бота", reply_markup=langugage_keyboard())

async def user_lang_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    





def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")


