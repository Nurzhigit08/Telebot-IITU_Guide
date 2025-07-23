import os
from dotenv import load_dotenv

import telebot
from telebot import types

load_dotenv()  # Загружаем переменные из .env
TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из переменной окружения

bot = telebot.TeleBot(TOKEN)

user_lang = {}  # user_id: 'ru' | 'kz' | 'en'
last_photo_message_id = {}  # Для хранения ID сообщений с фото
current_message_id = {}  # Для хранения ID текущего сообщения

# 📘 Переводы
translations = {
    'start_text': {
        'ru': "Здравствуйте!\nВыберите язык обращения!",
        'kz': "Сәлеметсіз бе!\nТілді таңдаңыз!",
        'en': "Hello!\nChoose language!"
    },
    'choose_category': {
        'ru': "Выберите категорию:",
        'kz': "Санатты таңдаңыз:",
        'en': "Choose category:"
    },
    'abiturient_menu': {
        'ru': "Что Вас интересует?",
        'kz': "Сізді не қызықтырады?",
        'en': "What are you interested in?"
    },
    'student_menu': {
        'ru': "Что вас интересует как студента?",
        'kz': "Сізді студент ретінде не қызықтырады?",
        'en': "What are you interested in as a student?"
    },
    'abiturient_docs': {
    'ru': (
        "*Перечень необходимых документов:*\n"
        " 1. Аттестат/диплом с приложением (оригинал)\n"
        " 2. Сертификат ЕНТ (эл. документ с сайта certificate.testcenter.kz)\n"
        " 3. 2 копии удостоверения личности\n"
        " 4. 8 фото 3х4 (каждое фото подписать с обратной стороны)\n"
        " 5. Мед. справка 075/У (со снимком флюорографии сроком не более 12 месяцев на дату зачисления 20.08.2025)\n"
        " 6. Карта профилактических прививок (форма 063/У)\n"
        " 7. Копия приписного свидетельства (для юношей)\n"
        " 8. Копия грамот и дипломов за последние три года"
    ),
    'kz': (
        "*Қажетті құжаттар тізімі:*\n"
        " 1. Аттестат/диплом және қосымшасы (түпнұсқа)\n"
        " 2. ҰБТ сертификаты (certificate.testcenter.kz сайтынан эл. құжат)\n"
        " 3. Жеке куәліктің 2 көшірмесі\n"
        " 4. 3x4 өлшеміндегі 8 фотосурет (артына аты-жөніңізді жазыңыз)\n"
        " 5. 075/У медициналық анықтамасы (20.08.2025 күнінен кешіктірілмеген флюорографиямен)\n"
        " 6. Екпе картасы (063/У форма)\n"
        " 7. Әскери тіркеу куәлігінің көшірмесі (ер балалар үшін)\n"
        " 8. Соңғы үш жылдағы марапаттар, дипломдар, IELTS 5.0+ немесе TOEFL 35+ сертификаттары"
    ),
    'en': (
        "*Required documents:*\n"
        " 1. Original certificate/diploma with transcript\n"
        " 2. UNT certificate (e-document from certificate.testcenter.kz)\n"
        " 3. 2 copies of ID card\n"
        " 4. 8 photos (3x4 cm) with name on the back\n"
        " 5. Medical certificate form 075/U (with fluorography not older than 12 months before 20.08.2025)\n"
        " 6. Immunization card (form 063/U)\n"
        " 7. Military registration certificate copy (for male applicants)\n"
        " 8. Copies of awards/diplomas (last 3 years), IELTS 5.0+ or TOEFL 35+ certificates"
    )
    },
    'study_info': {
        'ru': "Информация об учебе для студентов будет добавлена здесь.",
        'kz': "Студенттерге арналған оқу туралы ақпарат мұнда болады.",
        'en': "Study information for students will be added here."
    },
    'abiturient_price_caption': {
        'ru': '*Цены за обучение*',
        'kz': '*Оқу ақысы*',
        'en': '*Tuition fees*'
    },
    'abiturient_dates': {
        'ru': '''*Важные даты:*
        - Регистрация на ЕНТ: с 28 апреля до 14 мая
        - Работа Приемной комиссии: с 20 июня до 25 августа
        - Экзамен по английскому языку: с 20 июня до 25 августа
        - Подача документов: с 20 июня до 20 июля
        - Регистрация на конкурс грантов: с 13 июля по 20 июля
        - Подписание договора: с 15 августа до 25 августа
        - Прием заявлений на платное отделение: с 20 июня до 25 августа''',

        'kz': '''*Маңызды күндер:*
        - ҰБТ-ға тіркелу: 28 сәуірден 14 мамырға дейін
        - Қабылдау комиссиясының жұмысы: 20 маусымнан 25 тамызға дейін
        - Ағылшын тілі емтиханы: 20 маусымнан 25 тамызға дейін
        - Құжаттарды тапсыру: 20 маусымнан 20 шілдеге дейін
        - Грант байқауына тіркелу: 13 шілдеден 20 шілдеге дейін
        - Келісімшартқа қол қою: 15 тамыздан 25 тамызға дейін
        - Ақылы бөлімге өтініш қабылдау: 20 маусымнан 25 тамызға дейін''',

        'en': '''*Important Dates:*
        - Registration for UNT: from April 28 to May 14
        - Admission committee work: from June 20 to August 25
        - English exam: from June 20 to August 25
        - Document submission: from June 20 to July 20
        - Registration for grant competition: from July 13 to July 20
        - Contract signing: from August 15 to August 25
        - Applications for paid department: from June 20 to August 25'''
    },
    'abiturient_address': {
        'ru': "📍 *График работы:*\nПонедельник - Пятница\nс 9:00 до 18:00\n(Суббота и Воскресенье — выходные)\n\n📌 *Адрес:*\nГород Алматы, Манаса 34/1",
        'kz': "📍 *Жұмыс уақыты:*\nДүйсенбі - Жұма\nсағат 9:00-ден 18:00-ге дейін\n(Сенбі және Жексенбі — демалыс күндері)\n\n📌 *Мекенжай:*\nАлматы қаласы, Манас көшесі 34/1",
        'en': "📍 *Working hours:*\nMonday - Friday\nfrom 9:00 to 18:00\n(Saturday and Sunday — closed)\n\n📌 *Address:*\nAlmaty city, Manas 34/1"
    },
    'specialties_title': {
        'ru': "🎓 *Перечень специальностей*",
        'kz': "🎓 *Мамандықтар тізімі*",
        'en': "🎓 *List of specialties*"
    },
    'choose_program_group': {
        'ru': "Выберите группу образовательных программ:",
        'kz': "Білім беру бағдарламаларының тобын таңдаңыз:",
        'en': "Choose educational program group:"
    },
    'program_groups': {
        'ru': [
            "Информационные технологии",
            "Информационная безопасность",
            "Коммуникации и коммуникационные технологии",
            "Менеджмент и управление",
            "Финансы, экономика, банковское и страховое дело",
            "Журналистика и репортерское дело"
        ],
        'kz': [
            "Ақпараттық технологиялар",
            "Ақпараттық қауіпсіздік",
            "Коммуникациялар және коммуникациялық технологиялар",
            "Менеджмент және басқару",
            "Қаржы, экономика, банк және сақтандыру ісі",
            "Журналистика және репортерлік іс"
        ],
        'en': [
            "Information Technology",
            "Information Security",
            "Communications and Communication Technologies",
            "Management and Administration",
            "Finance, Economics, Banking and Insurance",
            "Journalism and Reporting"
        ]
    },
}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("1️⃣ Русский", callback_data='lang_ru'),
        types.InlineKeyboardButton("2️⃣ Қазақша", callback_data='lang_kz'),
        types.InlineKeyboardButton("3️⃣ English", callback_data='lang_en')
    )
    full_text = f"{translations['start_text']['ru']}\n\n{translations['start_text']['kz']}\n\n{translations['start_text']['en']}"
    bot.send_message(message.chat.id, full_text, reply_markup=markup)

# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    data = call.data
    lang = user_lang.get(user_id, 'ru')  # язык по умолчанию

    if data.startswith('lang_'):
        lang = data.split('_')[1]
        user_lang[user_id] = lang
        show_category(call.message, lang)

    elif data == 'category_student':
        show_student_options(call.message, lang)

    elif data == 'student_study':
        bot.send_message(call.message.chat.id, translations['study_info'][lang])

    elif data == 'abiturient_docs':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back",
            callback_data='category_abiturient'
        ))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=translations['abiturient_docs'][lang],
            reply_markup=markup,
            parse_mode='Markdown'
        )

    elif data == 'abiturient_prices':
        # Отправляем картинку с кнопкой "Назад" под ней
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back",
            callback_data='category_abiturient'
        ))
        
        with open('images/price.jpg', 'rb') as photo:
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=translations['abiturient_price_caption'][lang],
                reply_markup=markup,  # кнопка будет под картинкой
                parse_mode='Markdown'
            )
        
        # Удаляем старое сообщение с меню
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
    

    # Обработчик для перечня специальностей
    elif data == 'abiturient_programs':
        # Удаляем предыдущую картинку, если есть
        if 'last_photo' in user_lang and user_id in user_lang['last_photo']:
            try:
                bot.delete_message(call.message.chat.id, user_lang['last_photo'][user_id])
            except:
                pass
            del user_lang['last_photo'][user_id]
        
        # Отправляем новую картинку
        with open('images/spec.jpeg', 'rb') as photo:
            msg = bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=translations['specialties_title'][lang],
                parse_mode='Markdown'
            )
            # Сохраняем ID новой картинки
            if 'last_photo' not in user_lang:
                user_lang['last_photo'] = {}
            user_lang['last_photo'][user_id] = msg.message_id
        
        # Показываем группы программы
        show_program_groups(call.message, lang)
        
        # Удаляем предыдущее меню
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            print(f"Ошибка при удалении: {e}")

    elif data == 'category_abiturient':
        # При возврате в меню абитуриента удаляем картинку, если есть
        if 'last_photo' in user_lang and user_id in user_lang['last_photo']:
            try:
                bot.delete_message(call.message.chat.id, user_lang['last_photo'][user_id])
            except:
                pass
            del user_lang['last_photo'][user_id]
            
        if 'last_military_photo' in user_lang:
            try:
                bot.delete_message(call.message.chat.id, user_lang['last_military_photo'])
            except:
                pass
        
        # Показываем меню абитуриента
        show_abiturient_options(call.message, lang)
        
        # Удаляем текущее сообщение (с группами или деталями)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass

    # Обработчик для выбора группы программ
    elif data.startswith('program_group_'):
        group_index = int(data.split('_')[2])
        lang = user_lang.get(call.from_user.id, 'ru')
        group_name = translations['program_groups'][lang][group_index]
        
        # Редактируем сообщение с кнопками, показывая детали
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "⬅️ Назад к группам" if lang == 'ru' else "⬅️ Топтарға оралу" if lang == 'kz' else "⬅️ Back to groups",
            callback_data='abiturient_programs'
        ))
        
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"*{group_name}*\n\n{translations['program_details'][lang].get(group_name, 'Информация скоро будет добавлена')}",
                reply_markup=markup,
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Ошибка редактирования: {e}")

    elif data == 'abiturient_dates':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back",
            callback_data='category_abiturient'
        ))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=translations['abiturient_dates'][lang],
            reply_markup=markup,
            parse_mode='Markdown'
        )

    elif data == 'abiturient_address':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back",
            callback_data='category_abiturient'
        ))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=translations['abiturient_address'][lang],
            reply_markup=markup,
            parse_mode='Markdown'
    )
        
    elif data == 'abiturient_military':
        # Отправляем фото военной кафедры
        with open('images/military.jpeg', 'rb') as photo:
            msg = bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption="🪖 Военная кафедра" if lang == 'ru' else "🪖 Әскери кафедра" if lang == 'kz' else "🪖 Military department",
                parse_mode='Markdown'
                )
        user_lang['last_military_photo'] = msg.message_id # Сохраняем ID фото

        # Добавляем кнопку "Назад"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back", callback_data='category_abiturient'))
        # Редактируем текущее сообщение (оставляем только кнопку)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите действие:" if lang == 'ru' else "Әрекетті таңдаңыз:" if lang == 'kz' else "Choose an action:",
            reply_markup=markup
        )

    elif data in ['abiturient_back', 'student_back']:
        show_category(call.message, lang)

    elif data == 'back_to_start':
        start(call.message)

# Главное меню
def show_category(message, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("1️⃣ Абитуриент" if lang == 'ru' else "1️⃣ Талапкер" if lang == 'kz' else "1️⃣ Applicant", callback_data='category_abiturient'),
        types.InlineKeyboardButton("2️⃣ Студент" if lang == 'ru' else "2️⃣ Студент" if lang == 'kz' else "2️⃣ Student", callback_data='category_student'),
        types.InlineKeyboardButton("⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back", callback_data='back_to_start')
    )
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=translations['choose_category'][lang], reply_markup=markup)

# Абитуриент
def show_abiturient_options(message, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📄 Перечень документов" if lang == 'ru' else "📄 Құжаттар тізімі" if lang == 'kz' else "📄 Documents", callback_data='abiturient_docs'),
        types.InlineKeyboardButton("📍 Адрес и график работы" if lang == 'ru' else "📍 Мекенжай мен жұмыс уақыты" if lang == 'kz' else "📍 Address and schedule", callback_data='abiturient_address'),
        types.InlineKeyboardButton("📅 Важные даты" if lang == 'ru' else "📅 Маңызды күндер" if lang == 'kz' else "📅 Important dates", callback_data='abiturient_dates'),
        types.InlineKeyboardButton("💵 Цены за обучение" if lang == 'ru' else "💵 Оқу ақысы" if lang == 'kz' else "💵 Tuition fees", callback_data='abiturient_prices'),
        types.InlineKeyboardButton("🎓 Перечень специальностей" if lang == 'ru' else "🎓 Мамандықтар тізімі" if lang == 'kz' else "🎓 List of specialties", callback_data='abiturient_programs'),
        types.InlineKeyboardButton("🪖 Военная кафедра" if lang == 'ru' else "🪖 Әскери кафедра" if lang == 'kz' else "🪖 Military department", callback_data='abiturient_military'),
        types.InlineKeyboardButton("⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back", callback_data='abiturient_back')
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=translations['abiturient_menu'][lang],
        reply_markup=markup
    )
    
    # Удаляем предыдущее сообщение (если возможно)
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print(f"Ошибка при удалении предыдущего сообщения: {e}")

# Функция для показа групп образовательных программ
def show_program_groups(message, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Добавляем кнопки для каждой группы программ
    for i, group_name in enumerate(translations['program_groups'][lang]):
        markup.add(types.InlineKeyboardButton(
            group_name,
            callback_data=f'program_group_{i}'
        ))
    
    # Добавляем кнопку "Назад"
    markup.add(types.InlineKeyboardButton(
        "⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back",
        callback_data='category_abiturient'
    ))
    
    # Отправляем сообщение с выбором групп
    bot.send_message(
        chat_id=message.chat.id,
        text=translations['choose_program_group'][lang],
        reply_markup=markup
    )

#Abiturient_address
@bot.callback_query_handler(func=lambda call: call.data == 'abiturient_address')
def show_abiturient_address(call):
    lang = user_lang.get(call.from_user.id, 'ru')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back",
        callback_data='category_abiturient'
    ))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translations['abiturient_address'][lang],
        reply_markup=markup,
        parse_mode='Markdown'
    )


# Студент
def show_student_options(message, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📚 Учеба" if lang == 'ru' else "📚 Оқу" if lang == 'kz' else "📚 Study", callback_data='student_study'),
        types.InlineKeyboardButton("⬅️ Назад" if lang == 'ru' else "⬅️ Артқа" if lang == 'kz' else "⬅️ Back", callback_data='student_back')
    )
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=translations['student_menu'][lang], reply_markup=markup)

bot.polling(non_stop=True)