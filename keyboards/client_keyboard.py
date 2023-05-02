from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
# красота і дитині
markup.add('Продукти', 'Одяг', 'Подарунки').add(
    'Красота', 'Дитині', 'Аптека').add('Хімія', 'Господарство', 'Інше').add(
    'Статистика за місяць 📊').add('Минулий місяць')
