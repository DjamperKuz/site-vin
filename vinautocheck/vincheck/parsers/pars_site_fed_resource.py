import time
import main_pars
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


# Создание функции, которая забирает html-code для дальнейшего парсинга
def pars_site_fed_res(vin):
    # подключаем опции, для того, чтобы сайт думал, что пользователь реальный
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/"
                         "apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")

    # пробуем получить информацию, эмулируя клики и возврат данных
    try:
        browser = main_pars.get_browser('https://www.reestr-zalogov.ru/search/index', options=options)

        WebDriverWait(browser, 5).until(
            ec.element_to_be_clickable((By.LINK_TEXT, 'По информации о предмете залога'))).click()
        element = browser.find_element(By.ID, 'vehicleProperty.vin')
        element.send_keys(vin + Keys.RETURN)
        time.sleep(10)

        # Передаем хтмл код непосредственно из нотариальной палаты
        pagesource_not_palata = browser.page_source

        # Кликаем по "федеральному ресурсу" и передаем код страницы в переменную
        WebDriverWait(browser, 5).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Федеральный ресурс'))).click()
        
        pagesource_fed_resource = browser.page_source

    except Exception as ex:
        return ex

    finally:
        browser.close()
        browser.quit()

    def get_content(fed, palata):
        # объекты класса суп с парсером lxml
        soup_fed = BeautifulSoup(fed, "lxml")
        soup_palata = BeautifulSoup(palata, "lxml")
        try:
            # ищем информацию об отсутствии записей в реестре залогов
            fed_info = soup_fed.find('div', class_='search-error-label').text.strip()
            palata_info = soup_palata.find('div', class_='search-error-label').text.strip()

            # Создаем флаг для проверки того, что проверка не произошла и информация не была спарсена
            er = False
            if fed_info == 'Доступ запрещен. Запросы, поступившие с вашего IP-адреса, похожи на автоматические':
                er = True

            # создаем словарь для формирования json-file с полученными данными, и запись
            parsed_data = {"info_from_not_palata": palata_info,
                           "info_from_fed_resurs": fed_info,
                           "Error_inf": er}

        except Exception as ex:
            parsed_data = {"info_from_not_palata": "Нет информации по автомобилю",
                           "info_from_fed_resurs": "Нет информации по автомобилю",
                           "Error_inf": ex}

        return parsed_data

    return get_content(pagesource_fed_resource, pagesource_not_palata)


def main_fed_res():
    main_pars.save_json(pars_site_fed_res(main_pars.vin), 'fed_resource')


if __name__ == '__main__':
    main_fed_res()
