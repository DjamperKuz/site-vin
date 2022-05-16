import requests
import json
import time
from fake_useragent import UserAgent
# from vin_number.vinautocheck.vincheck.parsers.pars_settings import save_json


def parse_site_gibdd_api(vin):
    # счетчик времени выполнения функции, начальное время
    start_time = time.time()

    # словарь с ключами отправления запросов на АПИ
    keys_check = {
        "history": "history",
        "dtp": "aiusdtp",
        "wanted": "wanted",
        "restrict": "restricted",
        "diagnostic": "diagnostic"
    }

    # пустой словарь с формирующейся информацией
    info_check = {}

    # класс юзер агент для формирования рандомного для заголовков запроса
    ua = UserAgent()

    # выставляем количество попыток запросов
    limit = 5

    # проходим по каждому ключу в словаре
    for link in list(keys_check.keys()):

        # ссылка и заголовки для элемента link в цикле
        url = f'https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/{link}'
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-agent": f"{ua.random}"
        }

        # данные для POST запроса
        data = {
            "vin": vin,
            "checkType": keys_check[link]
        }

        # обнуление попыток для каждого прохода цикла и индикатор успешного выполнения запроса
        try_limit = 1
        tr = True

        # проверка условия, что запрос еще не выполнен успешно и количество попыток меньше указанного лимита (5)
        while tr and try_limit <= limit:

            # попытка получить информацию по запросу, если информация в req is None или ошибка Time out от сервера,
            # тогда итерация начинается заново
            try:
                print(f'Попытка №{try_limit}, key: {link}')
                req = requests.post(url, data=data, headers=headers)
                print(json.loads(req.text))
                info_check[link] = {}

                # попытка проверить успешный запрос, если в нем есть статус 200, тогда запрос успешный
                try:
                    info_check[link]["data"] = req.json()
                    if info_check[link]['data']['status'] == 200:
                        info_check[link]["success"] = True
                        tr = False
                        print('-'*40)

                    elif info_check[link]['data']['status'] == 404:
                        tr = False
                        info_check[link] = {}
                        info_check[link]["data"] = {"error_msg": "No info about auto"}
                        info_check[link]["success"] = True
                        print('-'*40)

                # Проверка, если попытки уже больше заданного лимита, тогда запрос не успешный и передается ошибка
                # Каждый раз увеличивается счетчик попыток
                except Exception as ex:
                    if try_limit > limit:
                        info_check[link] = {}
                        info_check[link]["success"] = False
                        info_check[link]["data"] = {"error_msg": f"{ex} or no info about car"}
                    print(f'errooorrr$$$$$$$  {ex}')
                    try_limit += 1

            except Exception as ex:
                if try_limit > limit:
                    info_check[link] = {}
                    info_check[link]["success"] = False
                    info_check[link]["data"] = {"error_msg": f"{ex} or no info about car"}
                print(f'errooorrr@@@@@@  {ex}')
                try_limit += 1

            finally:
                if try_limit > limit:
                    info_check[link] = {}
                    info_check[link]["success"] = False
                    info_check[link]["data"] = {"error_msg": "Try limit out (time is out) or no info about car"}

    print(f'Функция выполнилась за : {round(time.time() - start_time, 2)} сек')
    return info_check


def main_gibdd_api(vin_num):
    var_json = json.loads(json.dumps(parse_site_gibdd_api(vin_num)))
    return var_json
    # save_json(parse_site_gibdd_api(vin_num), 'data_gibdd_api')