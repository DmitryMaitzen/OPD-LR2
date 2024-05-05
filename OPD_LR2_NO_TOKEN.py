from time import sleep
from bs4 import BeautifulSoup
import requests
import telebot


def is_natural(string):
    try:
        int(string)
        if int(string) > 0:
            return True
    except ValueError:
        return False


def is_positive_float(string):
    try:
        float(string)
        if float(string) > 0:
            return True
    except ValueError:
        return False


def get_current_rate():
    page = requests.get("https://www.investing.com/currencies/usd-rub")
    soup = BeautifulSoup(page.text, "html.parser")
    data = soup.find("div", class_="mb-3 flex flex-wrap items-center gap-x-4 gap-y-2 md:mb-0.5 md:gap-6")
    current_rate = float(data.text[:7])
    return current_rate


def main():
    bot = telebot.TeleBot("ЗДЕСЬ_ДОЛЖЕН_БЫТЬ_ТОКЕН_ПОЛУЧЕННЫЙ_У_BOTFATHER")
    DEFAULT_UPPER_LIMIT = upper_limit = 100.0
    DEFAULT_LOWER_LIMIT = lower_limit = 90.0
    DEFAULT_DELAY_TIME = delay_time = 5

    @bot.message_handler(commands=["start"])
    def start_setting_parameters(message):
        bot.send_message(message.chat.id, "Привет! Давайте определимся с параметрами отслеживания курса доллара к рублю.")
        bot.send_message(message.chat.id, "Введите верхнюю границу в рублях (например, 97.6542):")
        bot.register_next_step_handler(message, set_upper_limit)
    def set_upper_limit(message):
        if is_positive_float(message.text):
            global upper_limit
            upper_limit = float(message.text)
            bot.send_message(message.chat.id, f"Отлично! Теперь верхняя граница составляет { upper_limit } руб.")
            bot.send_message(message.chat.id, "Введите нижнюю границу в рублях (например, 90.1234):")
            bot.register_next_step_handler(message, set_lower_limit)
        else:
            bot.send_message(message.chat.id, "Некорректные данные. Введите положительное вещественное число:")
            bot.register_next_step_handler(message, set_upper_limit)
    def set_lower_limit(message):
        if is_positive_float(message.text):
            global lower_limit
            lower_limit = float(message.text)
            bot.send_message(message.chat.id, f"Превосходно! Теперь нижняя граница составляет { lower_limit } руб.")
            bot.send_message(message.chat.id, "Введите задержку в секундах, с которой будет проверяться курс (например, 5):")
            bot.register_next_step_handler(message, set_delay_time)
        else:
            bot.send_message(message.chat.id, "Некорректные данные. Введите положительное вещественное число:")
            bot.register_next_step_handler(message, set_lower_limit)
    def set_delay_time(message):
        if is_natural(message.text):
            global delay_time
            delay_time = int(message.text)
            bot.send_message(message.chat.id, f"Очень хорошо! Теперь время задержки составляет { delay_time } сек.")
            get_help(message)
        else:
            bot.send_message(message.chat.id, "Некорректные данные. Введите натуральное число:")
            bot.register_next_step_handler(message, set_delay_time)

    @bot.message_handler(commands=["help"])
    def get_help(message):
        bot.send_message(message.chat.id, f"""Список команд.
/start: \"перезапустить\" бота и ввести все параметры вновь.
/help: получить настоящую справку.
/get: получить текущий курс.
/show: вывести текущие границы и интервал.
/default: установить параметры по умолчанию*.
/upper: задать верхнюю границу (руб.).
/lower: задать нижнюю границу (руб.).
/delay: задать задержку проверки курса (сек.).
/track: начать отслеживание.\n
*Параметры по умолчанию.
Верхняя граница: { DEFAULT_UPPER_LIMIT } руб.
Нижняя граница: { DEFAULT_LOWER_LIMIT } руб.
Задержка проверки: { DEFAULT_DELAY_TIME } сек.""")

    @bot.message_handler(commands=["get"])
    def send_current_rate(message):
        bot.send_message(message.chat.id, f"Текущий курс составляет { get_current_rate() } руб.")

    @bot.message_handler(commands=["show"])
    def show_parameters(message):
        global upper_limit, lower_limit, delay_time
        bot.send_message(message.chat.id, f"""Текущие значения параметров.
Верхняя граница: { upper_limit } руб.
Нижняя граница: { lower_limit } руб.
Задержка проверки курса: { delay_time } сек.""")

    @bot.message_handler(commands=["default"])
    def set_default_parameters(message):
        global upper_limit, lower_limit, delay_time
        upper_limit, lower_limit, delay_time = DEFAULT_UPPER_LIMIT, DEFAULT_LOWER_LIMIT, DEFAULT_DELAY_TIME
        bot.send_message(message.chat.id, f"""Установлены параметры по умолчанию.
Верхняя граница: { upper_limit } руб.
Нижняя граница: { lower_limit } руб.
Задержка проверки курса: { delay_time } сек.""")

    @bot.message_handler(commands=["upper"])
    def request_upper_limit(message):
        bot.send_message(message.chat.id, "Введите новую верхнюю границу в рублях (например, 98.7654) или \"Отмена\"/\"Cancel\" для отмены:")
        bot.register_next_step_handler(message, change_upper_limit)
    def change_upper_limit(message):
        global upper_limit
        if message.text == "Отмена" or message.text == "Cancel":
            bot.send_message(message.chat.id, f"Изменение верхней границы отменено. Текущее значение: { upper_limit } руб.")
        elif is_positive_float(message.text):
            upper_limit = float(message.text)
            bot.send_message(message.chat.id, f"Прекрасно! Теперь верхняя граница составляет { upper_limit } руб.")
        else:
            bot.send_message(message.chat.id, "Некорректные данные. Введите положительное вещественное число.")
            bot.register_next_step_handler(message, change_upper_limit)

    @bot.message_handler(commands=["lower"])
    def request_lower_limit(message):
        bot.send_message(message.chat.id, "Введите новую нижнюю границу в рублях (например, 89.0123) или \"Отмена\"/\"Cancel\" для отмены:")
        bot.register_next_step_handler(message, change_lower_limit)
    def change_lower_limit(message):
        global lower_limit
        if message.text == "Отмена" or message.text == "Cancel":
            bot.send_message(message.chat.id, f"Изменение нижней границы отменено. Текущее значение: { lower_limit } руб.")
        elif is_positive_float(message.text):
            lower_limit = float(message.text)
            bot.send_message(message.chat.id, f"Здорово! Теперь нижняя граница составляет { lower_limit } руб.")
        else:
            bot.send_message(message.chat.id, "Некорректные данные. Введите положительное вещественное число.")
            bot.register_next_step_handler(message, change_lower_limit)

    @bot.message_handler(commands=["delay"])
    def request_delay_time(message):
        bot.send_message(message.chat.id, "Введите новую задержку в секундах (например, 3) или \"Отмена\"/\"Cancel\" для отмены:")
        bot.register_next_step_handler(message, change_delay_time)
    def change_delay_time(message):
        global delay_time
        if message.text == "Отмена" or message.text == "Cancel":
            bot.send_message(message.chat.id, f"Изменение задержки отменено. Текущее значение: { delay_time } сек.")
        elif is_natural(message.text):
            delay_time = int(message.text)
            bot.send_message(message.chat.id, f"Замечательно! Теперь задержка составляет { delay_time } сек.")
        else:
            bot.send_message(message.chat.id, "Некорректные данные. Введите натуральное число.")
            bot.register_next_step_handler(message, change_delay_time)

    @bot.message_handler(commands=["track"])
    def request_tracking_time(message):
        bot.send_message(message.chat.id, "Введите время в секундах, в течение которого будет отслеживаться курс (например, 60), \
или \"Отмена\"/\"Cancel\" для отмены:")
        bot.register_next_step_handler(message, tracking)
    def tracking(message):
        if message.text == "Отмена" or message.text == "Cancel":
            bot.send_message(message.chat.id, "Отслеживание отменено.")
        else:
            if is_natural(message.text):
                tracking_time, time_passed = int(message.text), 0
                global upper_limit, lower_limit, delay_time
                bot.send_message(message.chat.id, "Отслеживание запущено.")
                while time_passed <= tracking_time:
                    current_rate = get_current_rate()
                    if current_rate > upper_limit:
                        bot.send_message(message.chat.id, f"Выход за верхнюю границу: { current_rate } руб.")
                    elif current_rate < lower_limit:
                        bot.send_message(message.chat.id, f"Выход за нижнюю границу: { current_rate } руб.")
                    time_passed += delay_time
                    if time_passed + delay_time < tracking_time:
                        sleep(delay_time)
                bot.send_message(message.chat.id, "Время отслеживания истекло.")
            else:
                bot.send_message(message.chat.id, "Некорректные данные. Введите натуральное число:")
                bot.register_next_step_handler(message, tracking)

    @bot.message_handler(content_types=["text"])
    def invalid_request(message):
        bot.send_message(message.chat.id, "Недействительный запрос. Список команд: /help.")

    bot.infinity_polling()


if __name__ == "__main__":
    main()
