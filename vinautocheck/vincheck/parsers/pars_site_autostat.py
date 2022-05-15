from .pars_settings import save_json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver as wier_webdriver


def pars_site_autoastat(vin):
    # подключение прокси
    proxy_options = {
        'proxy': {
            'https': 'http://rD2jWa:mkHcvE@138.59.206.220:9409'
        }
    }
    try:  # запуск и проверка сайта на работоспособность
        browser = wier_webdriver.Chrome(r"C:/VIN/vinautocheck/vincheck/chromedriver/chromedriver.exe",
                                        seleniumwire_options=proxy_options)
        browser.get(f'https://autoastat.com/en/')
        browser.set_page_load_timeout(20)
    except Exception as ex:
        car_info_autoastat = {
            'success': 'False',
            'info_autoastat': 'Сайт не работает'
        }
        return car_info_autoastat

    try:
        # клик на авторизацию
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                     'btn.btn-secondary.btn_mobile-unstyled'))).click()
        # авторизация на сайте
        username = browser.find_element(By.ID, '_username')
        password = browser.find_element(By.ID, '_password')
        username.send_keys('tomaslex@mail.ru')
        password.send_keys('Lz_ZYB4-Xqfj4uP')

        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-primary.btn-sm'))).click()

        elem = browser.find_element(By.ID, 'search_lot_by_identifier_form_field')  # вставляем VIN в строку
        elem.send_keys(vin + Keys.RETURN)
    except Exception as ex:
        car_info_autoastat = {
            'success': 'False',
            'info_autoastat': 'Сайт не работает'
        }
        return car_info_autoastat

    pagesource_autoastat = browser.page_source  # сохранение html кода страницы
    browser.close()
    browser.quit()

    def get_content(source):  # сбор информации с сайта
        try:
            soup = BeautifulSoup(source, 'lxml')

            car_left_data = [item.get_text(strip=True).replace('\n', '').replace(' ', '')
                             for item in soup.find('div', class_='card-vehicle').find_all('dd')]

            car_left_name = [item.get_text(strip=True).replace(' ', '_').replace(':', '')
                             for item in soup.find('div', class_='card-vehicle').find_all('dt')]

            car_mid_data = [item.get_text(strip=True).replace(' ', '_').replace(':', '')
                            for item in soup.find('div', class_='card full-height').find_all('dd')]

            car_mid_name = [item.get_text(strip=True).replace(' ', '_').replace(':', '')
                            for item in soup.find('div', class_='card full-height').find_all('dt')]

            car_right_data = [item.get_text(strip=True).replace(' ', '_').replace(':', '')
                              for item in soup.find('div', class_='card auction-card full-height').find_all('dd')]

            car_right_name = [item.get_text(strip=True).replace(' ', '_').replace(':', '')
                              for item in soup.find('div', class_='card auction-card full-height').find_all('dt')]

            car_info_autoastat = {
                'success': 'True',
                **dict(zip(car_left_name, car_left_data)),
                **dict(zip(car_mid_name, car_mid_data)),
                **dict(zip(car_right_name, car_right_data))
            }

            return car_info_autoastat

        except Exception as ex:
            car_info_autoastat = {
                'success': 'False',
                'info_autoastat': 'Нет информации'
            }

            return car_info_autoastat

    return get_content(pagesource_autoastat)  # работает


def main_autostat(vin):
    save_json(pars_site_autoastat(vin), 'data_autostat')

