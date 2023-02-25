from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
import os
from dotenv import load_dotenv
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from agregat_bot.tgbot.models.database import Person

load_dotenv()

storage = MemoryStorage()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


class MySG(StatesGroup):
    main = State()
    second = State()


async def get_data(dialog_manager: DialogManager, **kwargs):
    dialog_manager.current_context().dialog_data["dontshow"] = True
    dialog_manager.current_context().dialog_data["page"] = False
    data = dialog_manager.current_context().data
    print(data.get('username'))
    return {
        "name": data.get('username'),
    }

async def get_data_from_base(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().dialog_data
    dbpg = data.get('dbpage', 'none')
    return{
        'data': dbpg,
        "dontshow": data["dontshow"],
        "page": data["page"]
    }


async def button_pressed(c: CallbackQuery, button: Button, manager: DialogManager):
    manager.current_context().dialog_data["dontshow"] = False
    manager.current_context().dialog_data["page"] = True
    print(button)
    id = (int(button.widget_id)+1)*5
    print(id)
    result = Person.select()
    
    txt = ''
    for record in result[id-5:id]:
        txt += f"{record.id}\n"
        txt += f"{record.user_id}\n"
        txt += f"{record.user_name}\n"
        txt += f"{record.user_link}\n"
        txt += f"{record.group_id}\n"
        txt += f"{record.group_name}\n"
        txt += f"{record.group_link}\n"
        txt += f"{record.message_text}\n"
        txt += f"{record.media_files}\n"
        txt += f"{record.datatime}\n\n"
    manager.current_context().dialog_data["dbpage"] = txt
    

    
    # markup = c.message.reply_markup
    # await c.message.edit_text("qeqweq", reply_markup=markup)

def test_buttons_creator():
    data = Person.select()
    buttons = []
    for i in range(int(len(data) / 5)):
        i = str(i)
        buttons.append(Button(Const(int(i)+1), id=i, on_click=button_pressed))
    return buttons



async def go_next(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().next()

dialog = Dialog(
    Window(
        Format("Здравствуйте, чтобы получить данные из базы данных нажмите кнопку, {name}!"),
        Button(Const("Получить данные"), id="nothing", on_click=go_next),
        state=MySG.main,
        getter=get_data,  # here we set our data getter
    ),

    Window(
        Format("Данные из базы:", when="dontshow"),
        Format("{data}123", when="page"),
        ScrollingGroup(
            *test_buttons_creator(),
            id="numbers",
            width=3,
            height=3,),
        getter=get_data_from_base,
        state=MySG.second


    )
)
registry.register(dialog)

@dp.message_handler

@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK, data={"username": m.from_user.full_name})


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

