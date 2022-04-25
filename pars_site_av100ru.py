# Подключение библиотек для работы с запросами
import requests
import time
import json


# Создание функции с параметрами вин и апикеем
def pars_site_av100ru(vin, api):
    try:

        # попытка получить запрос из API, а далее проверка на наличие ошибок
        full_info_vin = requests.get(url=f'https://data.av100.ru/api.ashx?key={api}&vin={vin}').json()
        if full_info_vin["error"]:
            if full_info_vin["error_msg"] == 'Доступ истек':
                with open("data/av100ru.json", "w") as file:
                    json.dump(full_info_vin, file, indent=4, ensure_ascii=False, encoding='utf-8')
                exit("Доступ истек")
            elif full_info_vin["error_msg"] == 'Нет прав на запрошенный метод.':
                with open("data/av100ru.json", "w") as file:
                    json.dump(full_info_vin, file, indent=4, ensure_ascii=False, encoding='utf-8')
                exit("Нет прав на запрошенный метод.")
            elif full_info_vin["error_msg"] == 'Пользователь не найден.':
                with open("data/av100ru.json", "w") as file:
                    json.dump(full_info_vin, file, indent=4, ensure_ascii=False, encoding='utf-8')
                exit("Пользователь не найден.")
            elif full_info_vin["error_msg"] == 'Задан не коректный VIN.':
                with open("data/av100ru.json", "w") as file:
                    json.dump(full_info_vin, file, indent=4, ensure_ascii=False, encoding='utf-8')
                exit("Задан не корректный VIN.")
    except Exception as ex:
        return "#1 ", ex

    # создание переменной, которая будет передана далее для идентификации id задачи
    id_task = full_info_vin["result"]["taskid"]

    try:

        # Делаем запрос с айди, который был получен при первом запросе, и согласно документации av100ru делаем запросы
        # в которых ожидаем появление информации по url
        req = requests.get(f'https://data.av100.ru/fullapi.ashx?key={api}&taskid={id_task}&dates=1').json()
        count_try = 1
        while req["url"][:5] != 'https':
            req = requests.get(f'https://data.av100.ru/fullapi.ashx?key={api}&taskid={id_task}&dates=1').json()
            time.sleep(3)
            print(f"Try#{count_try}")
            count_try += 1

            # если в течении 35 секунд информацию не удалось получить, сохраняется информация с ошибкой и программа
            # заканчивается с ошибкой тайм-аут
            if count_try >= 8:
                with open("data/av100ru.json", "w") as file:
                    json.dump(req, file, indent=4, ensure_ascii=False, encoding='utf-8')
                exit("Time out")

        # происходит обработка битов маски, по которой можно узнать, информация по каким источникам присутствует в файле
        bits = 0
        maska = str(req["result"]["mask"])
        for item in maska:
            if item == '0':
                print(f"Не обработано, key id mask: {bits}")
            elif item == '1':
                print(f"Обработано успешно, key id mask: {bits}")
            else:
                print(f"Обработано не успешно, key id mask: {bits}")
            bits += 1
    except Exception as ex:
        return '#2 ', ex


    # записываем готовый запрос в json file
    try:
        with open("data/av100ru.json", "w", encoding='utf-8') as file:
            json.dump(requests.get(f'https://data.av100.ru/api.ashx?key={api}&vin={vin}').json, file, indent=4,
                      ensure_ascii=False)
    except Exception as ex:
        return '#3 ', ex


def main():
    code = 'Y6DTF698P80160129'
    apikey = 'APIKEY'
    pars_site_av100ru(code, apikey)


# Примерный VIN и APIKEY
if __name__ == '__main__':
    main()
