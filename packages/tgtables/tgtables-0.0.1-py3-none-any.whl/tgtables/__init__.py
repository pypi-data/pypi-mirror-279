import telebot
from telebot import types
import config


def create_first_table(data, current_page, total_pages):
    if data:
        start_index = (current_page - 1) * config.ROW_QUANTITY_ON_PAGE
        end_index = min(start_index + config.ROW_QUANTITY_ON_PAGE, len(data))
        response = f"Страница {current_page} из {total_pages}:\n\n"

        for number, element in list(enumerate(data, start=1))[start_index:end_index]:
            # Проверяем каждый элемент на None перед использованием
            response += f"{str(number)}. {' - '.join(str(el) for el in list(element.values())[1:])}\n"

        keyboard = types.InlineKeyboardMarkup()

            # Добавляем кнопки
        keyboard.row(
            types.InlineKeyboardButton("Назад", callback_data="back"),
            types.InlineKeyboardButton("Вперед", callback_data="forward"),
            types.InlineKeyboardButton("Перейти на страницу номер", callback_data="goto_page"),
        )
        keyboard.row(
            types.InlineKeyboardButton("Сортировать по названию (возрастание)", callback_data="sort_name_asc"),
            types.InlineKeyboardButton("Сортировать по названию (убывание)", callback_data="sort_name_desc"),
        )
        keyboard.row(
            types.InlineKeyboardButton("Сортировать по возрасту (возрастание)", callback_data="sort_age_asc"),
            types.InlineKeyboardButton("Сортировать по возрасту (убывание)", callback_data="sort_age_desc"),
        )
        keyboard.row(
            types.InlineKeyboardButton("Фильтровать по слову", callback_data="filter_by_word"),
            types.InlineKeyboardButton("Открыть карточку по номеру", callback_data="open_card_by_id"),
        )

    else:
        response = "Нет участников в базе данных"

    return response, keyboard


def update_contributors_message(data, chat_id, message_id, page, total_pages, bot):

    start_index = (page - 1) * config.ROW_QUANTITY_ON_PAGE
    end_index = min(start_index + config.ROW_QUANTITY_ON_PAGE, len(data))
    response = f"Страница {page} из {total_pages}:\n\n"

    nums_list = {}
    for number, element in list(enumerate(data, start=1)):
        nums_list[number] = element['id']

    num_id[chat_id] = nums_list
    print(num_id)

    for number, element in list(enumerate(data, start=1))[start_index:end_index]:
        # Проверяем каждый элемент на None перед использованием
        response += f"{str(number)}. {' - '.join(str(el) for el in list(element.values())[1:])}\n"

    keyboard = types.InlineKeyboardMarkup()

    # Добавляем кнопки
    keyboard.row(
        types.InlineKeyboardButton("Назад", callback_data="back"),
        types.InlineKeyboardButton("Вперед", callback_data="forward"),
        types.InlineKeyboardButton("Перейти на страницу номер", callback_data="goto_page"),
    )
    keyboard.row(
        types.InlineKeyboardButton("Сортировать по названию (возрастание)", callback_data="sort_name_asc"),
        types.InlineKeyboardButton("Сортировать по названию (убывание)", callback_data="sort_name_desc"),
    )
    keyboard.row(
        types.InlineKeyboardButton("Сортировать по возрасту (возрастание)", callback_data="sort_age_asc"),
        types.InlineKeyboardButton("Сортировать по возрасту (убывание)", callback_data="sort_age_desc"),
    )
    keyboard.row(
        types.InlineKeyboardButton("Фильтровать по слову", callback_data="filter_by_word"),
        types.InlineKeyboardButton("Открыть карточку по номеру", callback_data="open_card_by_id"),
    )

    try:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=response, reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException as e:
        if e.result_json['error_code'] == 400 and 'message to edit not found' in e.result_json['description']:
            # Сообщение не найдено, возможно, уже удалено
            print("Ошибка: Сообщение не найдено или уже удалено.")
        else:
            # Другая ошибка
            print(f"Ошибка API Telegram: {e}")


chat_pages = {}
main_message = {}
user_requests_goto_page = {}
user_requests_filter_by_word = {}
odd_messages = {}


def sort_callback_handler(call, data, bot):
    global response_list
    print(data)
    # Определяем параметры сортировки из callback'а
    sort_key = call.data.split('_')[1]  # Название параметра для сортировки
    reverse_sort = call.data.split('_')[2] == 'desc'  # Флаг для обратной сортировки

    if sort_key == 'name':
        response_list = sorted(data, key=lambda x: x['name'], reverse=reverse_sort)
    elif sort_key == 'age':
        response_list = sorted(data, key=lambda x: int(x['age']) if x['age'].isdigit() else 0,
                                    reverse=reverse_sort)

        # Обновляем сообщение с участниками на текущей странице
    current_page, total_pages = chat_pages.get(call.message.chat.id, (1, 1))
    update_contributors_message(response_list, call.message.chat.id, call.message.id, current_page, total_pages, bot)


def create_handlers(bot):
    bot.register_callback_query_handler(lambda call: callback_handler(call, bot), func=lambda call: True)
    #bot.register_message_handler(
    #    lambda message: handle_filter_by_word(message, bot),
    #    pass_bot=True
    #)
    #bot.register_message_handler(lambda message: handle_goto_page(message, bot), func=lambda message: message.chat.id in user_requests_goto_page,
    #                            pass_bot=True)


num_id = {}
def create_table(bot: telebot.TeleBot, data: list, row_names: list, message):

    if data:
        global response_list
        response_list1 = []
        response_list = []
        for element in data:
            el_dict = {row:el for row, el in zip(row_names, element)}
            response_list1.append(el_dict)

        nums_list = {}
        for number, element in list(enumerate(response_list1, start=1)):
            response_list.append(element)
            nums_list[number] = element['id']

        num_id[message.chat.id] = nums_list
        print(num_id)
        current_page = 1
        total_pages = (len(response_list) + 4) // 5

        chat_pages[message.chat.id] = (current_page, total_pages)
        response, keyboard = create_first_table(response_list, current_page, total_pages)
        main_message[message.chat.id] = bot.reply_to(message, response, reply_markup=keyboard).id
        create_handlers(bot)
        #bot.register_next_step_handler(message, lambda msg: create_common_handler(msg, bot))

    else:
        bot.reply_to(message, "Нет участников в базе данных")


def callback_handler(call, bot):
    # Переменные для пагинации

    odd_messages[call.message.chat.id] = []
    global chat_pages

    # Получаем текущую страницу и общее количество страниц из словаря по идентификатору чата
    current_page, total_pages = chat_pages.get(call.message.chat.id, (1, 1))
    # Проверяем, какая кнопка была нажата
    if call.data == 'back':
        current_page = max(current_page - 1, 1)
    elif call.data == 'forward':
        current_page = min(current_page + 1, total_pages)

    elif call.data.startswith('goto_page'):
        # Пользователь нажал кнопку "Перейти на страницу номер"
        # Отправляем запрос пользователю на ввод номера страницы

        odd_messages[call.message.chat.id].append(
            bot.send_message(call.message.chat.id, "Введите номер страницы:").id)


        # Сохраняем информацию о том, что пользователь хочет перейти на страницу

        user_requests_goto_page[call.message.chat.id] = call.message.id
        bot.register_next_step_handler(call.message, lambda msg: handle_goto_page(msg, bot))


        # odd_messages[call.message.chat.id].append(call.message.id)
    elif call.data.startswith('sort'):
        sort_callback_handler(call, response_list, bot)

    elif call.data == 'filter_by_word':
        user_requests_filter_by_word[call.message.chat.id] = call.message.id
        odd_messages[call.message.chat.id].append(bot.send_message(call.message.chat.id, "Введите ключевое слово для фильтрации:").id)
        bot.register_next_step_handler(call.message, lambda msg: handle_filter_by_word(msg, bot))

    elif call.data == 'open_card_by_id':
        odd_messages[call.message.chat.id].append(
            bot.send_message(call.message.chat.id, "Введите номер элемента:").id)



    # Обновляем сообщение с участниками
    update_contributors_message(response_list, call.message.chat.id, call.message.id, current_page, total_pages, bot)
    chat_pages[call.message.chat.id] = (current_page, total_pages)


def handle_goto_page(message, bot):

    global chat_pages
    current_page, total_pages = chat_pages.get(message.chat.id, (1, 1))
    odd_messages[message.chat.id].append(message.id)
    if message.text.isdigit() and int(message.text) <= total_pages:
        for msg in odd_messages[message.chat.id]:
            bot.delete_message(message.chat.id, msg)
        odd_messages[message.chat.id] = []
        # Получаем номер страницы, на которую пользователь хочет перейти
        page_number = int(message.text)

        # Удаляем информацию о запросе на переход на страницу
        message_id = user_requests_goto_page.pop(message.chat.id, None)

        # Обновляем сообщение с участниками
        update_contributors_message(response_list, message.chat.id, message_id, page_number, total_pages, bot)
        chat_pages[message.chat.id] = (page_number, total_pages)

    else:
        odd_messages[message.chat.id].append(
            bot.send_message(message.chat.id, "Укажите корректный номер страницы").id)
        bot.register_next_step_handler(message, lambda msg: handle_goto_page(msg, bot))




def handle_filter_by_word(message, bot):

    global response_list
    keyword = message.text.lower()
    filtered_list = [element for element in response_list if keyword in element['name'].lower()
                     or keyword in element['username'].lower() or keyword in element['role'].lower()]
    response_list = filtered_list
    current_page = 1
    total_pages = (len(response_list) + 4) // 5
    chat_pages[message.chat.id] = (current_page, total_pages)

    update_contributors_message(filtered_list, message.chat.id, main_message[message.chat.id], current_page,
                                total_pages, bot)
    odd_messages[message.chat.id].append(message.id)
    for msg in odd_messages[message.chat.id]:
        bot.delete_message(message.chat.id, msg)
    user_requests_filter_by_word.pop(message.chat.id, None)



def handle_card_id(message, bot):

    odd_messages[message.chat.id].append(message.id)
    if message.text.isdigit():
        for msg in odd_messages[message.chat.id]:
            bot.delete_message(message.chat.id, msg)
        odd_messages[message.chat.id] = []
        # Получаем номер страницы, на которую пользователь хочет перейти
        page_number = int(message.text)

        # Удаляем информацию о запросе на переход на страницу
        message_id = user_requests_goto_page.pop(message.chat.id, None)

        # Обновляем сообщение с участниками
        update_contributors_message(response_list, message.chat.id, message_id, page_number, total_pages, bot)
        chat_pages[message.chat.id] = (page_number, total_pages)

    else:
        odd_messages[message.chat.id].append(
            bot.send_message(message.chat.id, "Укажите корректный номер страницы").id)

    user_requests_goto_page.pop(message.chat.id, None)

