import time
import main_pars
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pars_site_gost(vin):
    options = main_pars.webdriver.ChromeOptions()
    options.add_argument("--headless")  # включение фонового режима работы браузера
    try:
        browser = main_pars.get_browser('https://easy.gost.ru/', options)
    except Exception as ex:
        car_info_gost = {
            'success': 'False',
            'info_gost': 'Сайт не работает',
        }
        return car_info_gost

    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "btnFindVin")))
        elem = browser.find_element(By.ID, 'findVin')  # вставляем VIN в строку
        elem.send_keys(vin + Keys.RETURN)
    except Exception as ex:
        car_info_gost = {
            'success': 'False',
            'info_gost': 'Сайт не работает',
        }
        return car_info_gost

    time.sleep(2)
    pagesource_gost = browser.page_source
    browser.close()
    browser.quit()

    def get_content(source):
        try:
            soup = BeautifulSoup(source, "lxml")

            car_info = dict(zip([
                'condition', 'VIN', 'revocable_company', 'organizer_revocable',
                'stamp', 'name_vehicle', 'reasons_recall', 'works_recommendations'],
                [item for i, item in enumerate(soup.find('div', class_='div-revocamp').
                                               stripped_strings, 1) if i % 2 == 1]))
            car_info_gost = {'success': 'True', **car_info}
        except Exception as ex:
            car_info_gost = {
                'success': 'True',
                'info_gost': 'Не найден среди отзывных кампаний',
            }

        return car_info_gost

    return get_content(pagesource_gost)  # работает


def main_gost(vin):
    main_pars.save_json(pars_site_gost(vin), 'data_gost')



