import main_pars
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# testing

def pars_site_vinfax(vin):
    try:
        # открываем драйвер, передаём ему ссылку
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)
        url = "https://vinfax.site/"
        name = "q"
        driver.get(url)
        # driver.maximize_window()

        # вводим vin
        vin_imput = driver.find_element(by=By.NAME, value=name)
        vin_imput.clear()
        vin_imput.send_keys(vin)
        vin_imput.send_keys(Keys.ENTER)
        time.sleep(2)

        to_parse = driver.page_source
        soup_to_rapse = BeautifulSoup(to_parse, "lxml")
        to_parse = soup_to_rapse.find(class_="main__item_img")

        car_all_data = {}
        if to_parse is not None:
            # получаем в переменную весь код страницы
            src_begin = driver.page_source
            soup_begin = BeautifulSoup(src_begin, "lxml")
            new_url = "https://vinfax.site/" + soup_begin.find(class_="main__item").find("a").get("href")
            driver.get(new_url)

            src = driver.page_source

            # создаём объект супа
            soup = BeautifulSoup(src, "lxml")

            # спарсили название машины
            car_title = soup.find(class_="auto__foto_title").text.strip()

            # смотрим наличие записей по автомобилю

            # достали данные из таблицы
            car_table_info = soup.find(class_="info-tabcontent").find("table").find("tbody").find_next("tr").find_next(
                "tr").find_all("td")

            # список нежелательных символов
            rep = ["\n", " "]

            # убираем неразрывный пробел
            for i in range(2):
                car_table_info[i] = str(car_table_info[i].text).strip()
                if " " in car_table_info[i]:
                    car_table_info[i] = car_table_info[i].replace(" ", " ")

            # записываем наши данные в отдельный переменные
            source = car_table_info[0]

            # вспомогательные переменные
            counter = 0
            to_skeep = False

            # списки ошибок при расшифровке vin, которые нам нужно игнорировать
            list_of_errors_in_meaning = ["Not Applicable"]
            list_of_errors_in_head = ["Error", "Possible Values", "V I N", "Model Year", "Model", "Transmission Style",
                                      "VIN"]

            # создаём два списка. Первый содержит ключи нашего будущего словаря, второй - значения
            # пробегаемся так по всей таблице. Если данные нас удовлетворяют, создаём словарь
            car_VIN_table_info_head = []
            car_VIN_table_info_meaning = []
            car_VIN_table_info_dictionary = {}
            car_VIN_table_info = soup.find(class_="info-tabcontent").find_next(class_="info-tabcontent").find("table")\
                .find("tbody").find_all("tr")

            for item in car_VIN_table_info:
                item = str(item.text).strip()
                num_of_slice = item.index(":")

                car_VIN_table_info_head.append(item[0:num_of_slice])
                car_VIN_table_info_meaning.append(item[num_of_slice + 2:])

                for item1 in list_of_errors_in_head:
                    if item1 in car_VIN_table_info_head[counter]:
                        car_VIN_table_info_head[counter] = ""
                        car_VIN_table_info_meaning[counter] = ""
                        to_skeep = True

                        counter += 1
                        break

                if to_skeep:
                    to_skeep = False
                    continue

                for item2 in list_of_errors_in_meaning:
                    if item2 in car_VIN_table_info_meaning[counter]:
                        car_VIN_table_info_head[counter] = ""
                        car_VIN_table_info_meaning[counter] = ""
                        to_skeep = True

                        counter += 1
                        break

                if to_skeep:
                    to_skeep = False
                    continue

                for item1 in rep:
                    if item1 in car_VIN_table_info_meaning[counter]:
                        car_VIN_table_info_meaning[counter] = car_VIN_table_info_meaning[counter].replace(item1, "")

                for item1 in rep:
                    if item1 in car_VIN_table_info_head[counter]:
                        car_VIN_table_info_head[counter] = car_VIN_table_info_head[counter].replace(item1, "")

                if counter + 1 == len(car_VIN_table_info):
                    for i in range(len(car_VIN_table_info_head)):
                        car_VIN_table_info_dictionary[car_VIN_table_info_head[i]] = car_VIN_table_info_meaning[i]
                    car_VIN_table_info_dictionary.pop("")
                    break

                counter += 1

            counter = 0

            # создаём два списка. Первый содержит ключи нашего будущего словаря, второй - значения
            # пробегаемся так по всей таблице. Если данные нас удовлетворяют, создаём словарь
            car_detailes_head = []
            car_detailes_meaning = []
            car_detailes_dictionary = {}
            car_detailes_to_delete = ["<li><span>", "</li>", "/span>"]
            car_detailes = soup.find(class_="auto__descr_list").find_all("li")
            for item in car_detailes:
                item = str(item).strip()
                for item1 in car_detailes_to_delete:
                    if item1 in item:
                        item = item.replace(item1, "")

                num_of_slice = item.index(":")

                car_detailes_head.append(item[0:num_of_slice])
                car_detailes_meaning.append(item[num_of_slice + 2:])

                if counter + 1 == len(car_detailes):
                    for i in range(len(car_detailes_head)):
                        if " " in car_detailes_meaning[i]:
                            car_detailes_meaning[i] = car_detailes_meaning[i].replace(" ", " ")
                        car_detailes_dictionary[car_detailes_head[i]] = car_detailes_meaning[i]
                        if (car_detailes_dictionary[car_detailes_head[i]] == "") or (
                                car_detailes_dictionary[car_detailes_head[i]] == " ") or (
                                car_detailes_head[i] == "VIN") or (car_detailes_head[i] == "Производитель"):
                            car_detailes_dictionary.pop(car_detailes_head[i])
                    break

                counter += 1

            counter = 1

            # парсим фотографии машины, сохраняем ссылки на них(есть вотер марки)
            car_photoes_head = []
            car_photoes_meaning = []
            car_photoes_dictionary = {}
            car_photoes = soup.find_all(class_="carousel-item")
            for item in car_photoes:
                item = str(item)
                photo_index_start = item.find("src=")
                photo_index_end = item.find(".jpg")
                car_photo_src = item[photo_index_start + 5:photo_index_end + 4]
                car_photo_src = "https://vinfax.site/" + car_photo_src

                car_photoes_head.append(f"car_photo_number_{counter}")
                car_photoes_meaning.append(car_photo_src)

                if counter == len(car_photoes):
                    for i in range(len(car_photoes_head)):
                        car_photoes_dictionary[car_photoes_head[i]] = car_photoes_meaning[i]

                counter += 1

            # создание словаря с детальной историей
            car_detailed_history = {"title": car_title,
                                    "source": source}

            # объединяем все наши словари в один
            car_all_data = {**car_detailed_history, **car_VIN_table_info_dictionary, **car_detailes_dictionary,
                            **car_photoes_dictionary}

            return True, car_all_data
        else:
            return False, car_all_data

    except Exception as ex:
        # вывод ошибки в консоль в случае её наличия
        print(ex)
    finally:
        # закрываем драйвер
        driver.close()
        driver.quit()


def main_vinfax():
    main_pars.save_json(pars_site_vinfax(main_pars.vin), 'data_vinfax')


if __name__ == "__main__":
    main_vinfax()
