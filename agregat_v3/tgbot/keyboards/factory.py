from aiogram.filters.callback_data import CallbackData

# category_button = CallbackData('category', 'parent_id', 'child_id', 'parent_name', 'child_name', 'match_words')

class CategoryData(CallbackData, prefix='category'):
    parent_id: str
    child_id: str
    parent_name: str
    child_name: str
    match_words: str