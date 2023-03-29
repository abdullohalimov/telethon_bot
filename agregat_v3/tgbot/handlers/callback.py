from aiogram.types import CallbackQuery
from tgbot.keyboards.factory import CategoryData
from aiogram import Router, Bot
from tgbot.models.database import Person


custom_couter = Router()

@custom_couter.callback_query(CategoryData.filter())
async def my_callback_foo(query: CallbackQuery, callback_data: CategoryData, ):
    print("bar =", callback_data.child_name)

@custom_couter.callback_query()
async def callback_handler(callback: CallbackQuery, bot: Bot):
    if callback.message.entities != None:
        msgtype = 'text'
        group_id = callback.message.entities[3].extract_from(callback.message.text)
        message_id = callback.message.entities[-1].extract_from(callback.message.text)    
    else:
        msgtype = 'caption'
        group_id = callback.message.caption_entities[3].extract_from(callback.message.caption)
        message_id = callback.message.caption_entities[-1].extract_from(callback.message.caption)
    
    if callback.data == "delete":
        record: Person = Person.get(Person.message_id==message_id, Person.group_id==group_id)
        print(record.message_text)
        record.delete_instance()
        record.save()
        
        await callback.message.delete()
            


