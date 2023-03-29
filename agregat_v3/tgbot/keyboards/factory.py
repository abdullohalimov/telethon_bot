from aiogram.filters.callback_data import CallbackData

# category_button = CallbackData('category', 'parent_id', 'child_id', 'parent_name', 'child_name', 'match_words')


class CategoryKeyboard(CallbackData, prefix='CatKeyb'):
    cat: str
    
class CategoryData(CallbackData, prefix='category'):
    category: str


