from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent
from datetime import datetime
from vin_number.vinautocheck.vincheck.parsers.pars_settings import save_json

def parse_site_fed_resource(vin_code):
    # создание объекта юзер агент для формирования заголовка с рандомным юзер-агентом
    ua = UserAgent()
    s = Service(executable_path="chromedriver/chromedriver.exe")

    # оформление опций для дальнейшей работы вебдрайвера
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua}")
    options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,"
                         "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")

    # открытие браузера
    browser = webdriver.Chrome(service=s,
                               options=options)

    # переход по ссылке, получение хтмл кода двух страниц - федерального ресурса и нотариальной палаты
    try:
        browser.get('https://www.reestr-zalogov.ru/search/index')

        WebDriverWait(browser, 5).until(
            ec.element_to_be_clickable((By.LINK_TEXT, 'По информации о предмете залога'))).click()
        element = browser.find_element(By.ID, 'vehicleProperty.vin')
        element.send_keys(vin_code + Keys.RETURN)
        time.sleep(5)

        pagesource_not_palata = browser.page_source
        WebDriverWait(browser, 5).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Федеральный ресурс'))).click()
        pagesource_fed_resource = browser.page_source

        return pagesource_fed_resource, pagesource_not_palata

    except Exception as ex:
        parsed_data = {"success": False,
                       "data": {
                           "info_from_not_palata": "1@Ошибка",
                           "info_from_fed_resurs": "1@Ошибка",
                           "error_info": ex,

                           "time": str(datetime.time(datetime.now()))
                       }
                       }
        return parsed_data

    finally:
        browser.close()
        browser.quit()


def get_info(vin):
    # работа с хтмл кодом, парс информации из хтмл кода
    data = parse_site_fed_resource(vin)
    fed_res, not_palata = data[0], data[1]

    soup_fed = BeautifulSoup(fed_res, "lxml")
    soup_palata = BeautifulSoup(not_palata, "lxml")
    try:
        # поиск в html коде по двум страничкам, в случае присутствия каких-либо сведений (т.е. отсутствия таблички об
        # отсутствии информации) формируется информация по наличию машины в залоге

        try:
            fed_info = soup_fed.find('div', class_='search-error-label')
            palata_info = soup_palata.find('div', class_='search-error-label')

            er = False

            if fed_info is None or palata_info is None:
                return {
                    "success": True,
                    "data": {"info_from_not_palata": "Возможно, машина находится в залоге",
                             "info_from_fed_resurs": "Возможно, машина находится в залоге",
                             "error_inf": er,
                             "time": str(datetime.time(datetime.now()))
                             }
                }

            fed_info = fed_info.text.strip()
            palata_info = palata_info.text.strip()

            if fed_info == 'Доступ запрещен. Запросы, поступившие с вашего IP-адреса, похожи на автоматические' or \
                    palata_info == 'Доступ запрещен. Запросы, поступившие с вашего IP-адреса, похожи на автоматические':
                er = True
                return {"success": False,
                        "data": {"info_from_not_palata": palata_info,
                                 "info_from_fed_resurs": fed_info,
                                 "error_inf": er,
                                 "time": str(datetime.time(datetime.now()))
                                 }
                        }
        except Exception as ex:
            return {"success": False,
                    "data": {
                        "info_from_not_palata": '2@Ошибка',
                        "info_from_fed_resurs": '2@Ошибка',
                        "error_inf": ex,
                        "time": str(datetime.time(datetime.now()))
                    }
                    }

        return {"data": {"info_from_not_palata": palata_info,
                         "info_from_fed_resurs": fed_info,
                         "error_inf": er,
                         "time": str(datetime.time(datetime.now()))
                         },
                "success": True
                }

    except Exception as ex:
        return {"data": {"info_from_not_palata": "3@Ошибка",
                         "info_from_fed_resurs": "3@Ошибка",
                         "error_inf": ex,
                         "time": str(datetime.time(datetime.now()))
                         },
                "success": False
                }


def main_fed_resource(vin):
    save_json(get_info(vin), 'data_fed_resource')


main_fed_resource('XTA21144094786239')
