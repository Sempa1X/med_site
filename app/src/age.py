# Производит расчет возроста для медицинских целей
# Отдает либо "сколько полных лет" если лет > 0
# Либо "сколько полных месяцев" если месяцев > 0
# Либо "сколько полных дней" с учетом високосных февралей

import calendar
from datetime import datetime
from datetime import date


def calculate_age(birth_year, birth_month, birth_day):  # Расчет "Полных лет"
    born = datetime(birth_year, birth_month, birth_day)
    today = date.today()
    full_year = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def corrector():  # Количество дней в месяце
        if born.month in (1, 3, 5, 7, 8, 10, 12):
            spec = 31
        elif born.month in (4, 6, 9, 11):
            spec = 30
        elif born.month == 2 and calendar.isleap(born.year) is True:  # Для високосного февраля
            spec = 29
        elif born.month == 2 and calendar.isleap(born.year) is False:  # Для обычного февраля
            spec = 28
        else:
            spec = 'Ошибка'
        print(spec)
        return spec

    def year_suffix(num):  # Определение: год/года/лет
        if int(num) in (11, 12, 13, 14):
            res = ' лет'
        else:
            if int(str(num)[-1]) in (2, 3, 4):
                res = ' года'
            elif int(str(num)[-1]) == 1:
                res = ' год'
            elif int(str(num)[-1]) in (0, 5, 6, 7, 8, 9):
                res = ' лет'
            else:
                res = ''
        return res

    if full_year > 0:  # Полных лет
        age = str(full_year) + year_suffix(full_year)
    elif full_year == 0:  # Полных месяцев
        full_month = today.month - born.month - (today.day < born.day)

        if full_month > 0:
            age = str(full_month) + ' мес.'
        elif full_month < 0:
            age = str(full_month + 12) + ' мес.'
        elif full_month == 0:  # Полных дней
            if today.day - born.day > 0:
                age = str(today.day - born.day) + ' дн.'
            else:
                age = 'Эмбрион???'
        else:
            age = 'Эмбрион???'
    else:
        age = 'Эмбрион???'
    return age

# --- Тестове данные
# birth_year = 2021
# birth_month = 7
# birth_day = 1
# print(calculate_age(birth_year, birth_month, birth_day))