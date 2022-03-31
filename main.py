"""Проект: сайт с поиском автомобильных номеров"""
import time
import lxml
import json
import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver as wier_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


def pars_site_gibdd(vin, options):  # парсинг сайта ГИБДД, возвращает dict с информацией о машине
    try:  # запуск и проверка сайта на работоспособность
        browser = webdriver.Chrome(r"C:\chromedriver\chromedriver.exe", options=options)
        browser.get('https://xn--90adear.xn--p1ai/check/auto')
        browser.set_page_load_timeout(10)
    except Exception as ex:
        car_info_gibdd = {'info_gibdd': 'Сайт не работает',
                          'error_gibdd': str(ex)
                          }
        return car_info_gibdd

    def skip_ads():  # закрывает рекламу если видео, если просто картинка, то ждёт
        try:
            WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "close_modal_window"))).click()
        except:
            time.sleep(4)

    try:  # вставляем VIN в строку
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "checker")))
        elem = browser.find_element(By.ID, 'checkAutoVIN')
        elem.send_keys(vin + Keys.RETURN)
    except Exception as ex:
        car_info_gibdd = {'info_gibdd': 'Сайт не работает',
                          'error_gibdd': str(ex)
                          }
        return car_info_gibdd

    # кнопки с сайта, на которые нужно нажать, чтобы получить информацию
    buttons = ["запросить сведения о периодах регистрации", "запросить сведения о ДТП", "запросить сведения о розыске",
               "запросить сведения об ограничениях"]

    for button in range(len(buttons)):  # нажатие на все кнопки с информацией
        WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, buttons[button]))).click()
        skip_ads()

    # WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "запросить сведения о ДК"))).click()
    # skip_ads()

    pagesource_gibdd = browser.page_source  # сохранение html кода страницы
    browser.close()
    browser.quit()

    def get_content(source):  # сбор информации с сайта
        soup = BeautifulSoup(source, "lxml")

        # сбор информации о регистрации в гибдд
        car_info_reg = {}
        try:
            soup_reg = soup.find('div', id='checkAutoHistory', class_='checkAutoSection')\
                                .find('ul', class_='fields-list vehicle')
            car_info_reg['reg'] = dict(zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_') for item in
                                            soup_reg.find_all('span', class_='caption')],
                                           [item.get_text(strip=True).replace('\n', '') for item in
                                            soup_reg.find_all('span', class_='field')]))
        except Exception as ex:
            car_info_reg['reg'] = {'info_reg': 'Нет информации',
                                   'error_reg': str(ex)}

        # сбор информации о дтп
        car_info_dtp = {}
        dtp_dict = {}
        try:
            text = 'В результате обработки запроса к АИУС ГИБДД записи о дорожно-транспортных происшествиях не найдены.'
            if text in soup.find('div', id='checkAutoContainer').get_text():
                car_info_dtp['dtp'] = {'info_dtp': text}
            else:
                soup_dtp = soup.find('div', id='checkAutoAiusdtp', class_='checkAutoSection')\
                                    .find('ul', class_='aiusdtp-list').find_all('ul', class_='fields-list aiusdtp-data')

                soup_dtp_number = soup.find('div', id='checkAutoAiusdtp',
                                            class_='checkAutoSection').find_all('p', class_='ul-title')

                for i, number in enumerate(soup_dtp_number):
                    dtp_dict[f'dtp_№_{i}'] = number.get_text()

                for i, object in enumerate(soup_dtp):
                    dtp_dict[f'dtp_{i}'] = dict(
                        zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_') for item in
                             object.find_all('span', class_='caption')],
                            [item.get_text(strip=True).replace('\n', '') for item in
                             object.find_all('span', class_='field')]))

                car_info_dtp['dtp'] = dtp_dict
        except Exception as ex:
            car_info_dtp['dtp'] = {'info_dtp': 'Сервис не работает',
                                   'error_dtp': str(ex)}

        # сбор информации о розыске
        car_info_roz = {}
        roz_dict = {}
        try:
            text = 'По указанному VIN (номер кузова или шасси) не найдена информация о розыске транспортного средства.'
            if text in soup.find('div', id='checkAutoContainer').get_text():
                car_info_roz['roz'] = {'info_roz': text}
            else:
                soup_roz = soup.find('div', id='checkAutoWanted', class_='checkAutoSection')\
                    .find('ul', class_='wanted-list').find_all('ul', class_='fields-list wanted-data')

                soup_roz_number = soup.find('div', id='checkAutoWanted',
                                            class_='checkAutoSection').find_all('p', class_='ul-title')

                for i, number in enumerate(soup_roz_number):
                    roz_dict[f'roz_№_{i}'] = number.get_text()

                for i, object in enumerate(soup_roz):
                    roz_dict[f'roz_{i}'] = dict(
                        zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_') for item in
                             object.find_all('span', class_='caption')],
                            [item.get_text(strip=True).replace('\n', '') for item in
                             object.find_all('span', class_='field')]))

                    car_info_roz['roz'] = roz_dict
        except Exception as ex:
            car_info_roz['roz'] = {'info_roz': 'Сервис не работает',
                                   'error_roz': str(ex)}

        # сбор информации о наложенных ограничениях
        ogran_dict = {}
        car_info_ogran = {}
        try:
            text = '''По указанному VIN (номер кузова или шасси) не найдена информация о наложении ограничений на 
            регистрационные действия с транспортным средством.'''
            if text in soup.find('div', id='checkAutoContainer').get_text():
                car_info_ogran['ogran'] = {'info_ogran': text}
            else:
                soup_ogran = soup.find('div', id='checkAutoRestricted', class_='checkAutoSection')\
                    .find('ul', class_='restricted-list').find_all('ul', class_='fields-list restrict-data')

                for i, object in enumerate(soup_ogran):
                    ogran_dict[f'ogran_{i}'] = dict(
                        zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_') for item in
                             object.find_all('span', class_='caption')],
                            [item.get_text(strip=True).replace('\n', '') for item in
                             object.find_all('span', class_='field')]))

                car_info_ogran['ogran'] = ogran_dict
        except Exception as ex:
            car_info_ogran['ogran'] = {'info_ogran': 'Сервис не работает',
                                       'error_ogran': str(ex)}

        return dict(**car_info_reg, **car_info_dtp, **car_info_roz, **car_info_ogran)

    return get_content(pagesource_gibdd)  # работает, добавить периоды владения


def pars_site_bidfax(vin):  # парсинг сайта bidfax, возвращает dict с информацией о машине
    try:  # запуск и проверка сайта на работоспособность
        browser = webdriver.Chrome(r"C:\chromedriver\chromedriver.exe")
        browser.get(f"https://bidfax.info/")
        browser.set_page_load_timeout(10)
    except Exception as ex:
        car_info_bidfax = {'info_bidfax': 'Сайт не работает',
                           'error_bidfax': str(ex)}
        return car_info_bidfax

    elem = browser.find_element(By.ID, 'search')  # вставляем VIN в строку
    elem.send_keys(vin + Keys.RETURN)

    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click()
        for i in range(5):  # прогрузка всех фото машины
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                         "fotorama__arr.fotorama__arr--next"))).click()
        time.sleep(5)
    except Exception as ex:
        car_info_bidfax = {'info_bidfax': 'Нет информации',
                           'error_bidfax': str(ex)
                           }
        return car_info_bidfax

    pagesource_bidfax = browser.page_source  # сохранение html кода страницы
    browser.close()
    browser.quit()

    def get_content(source):  # сбор информации с сайта
        soup = BeautifulSoup(source, "lxml")

        car_photo = soup.find('div', class_='fotorama__nav__shaft fotorama__grab')
        car_info = soup.find('div', class_='col-md-3 full-right')

        # сбор информации о машине
        car_info_bidfax = dict(zip([
            'lot_number_bidfax', 'date_of_sale_bidfax', 'year_of_release_bidfax', 'VIN_bidfax',
            'status_bidfax', 'engine_bidfax', 'mileage_bidfax',
            'seller_bidfax', 'documents_bidfax', 'place_of_sale_bidfax', 'primary_damage_bidfax',
            'secondary_damage_bidfax',
            'est._retail_value_dollars_bidfax', 'repair_price_dollars_bidfax', 'transmission_bidfax',
            'color_bidfax', 'drive_bidfax', 'fuel_bidfax', 'keys_bidfax', 'notes_bidfax'],
            [item.get_text(strip=True) for item in car_info.find_all("span", class_="blackfont")]))
        try:
            car_info_bidfax['auction_bidfax'] = soup.find('span', class_='copart').get_text(strip=True)
        except:
            car_info_bidfax['auction_bidfax'] = soup.find('span', class_='iaai').get_text(strip=True)

        # сбор фотографий
        photo = ['https://bidfax.info/' + item.get('src') for item in car_photo.find_all('img')]
        for i in range(1, len(photo) + 1):
            car_info_bidfax[f'car_photo_number_{i}'] = photo[i - 1]

        return car_info_bidfax

    return get_content(pagesource_bidfax)  # работает


def pars_site_nicb(vin, options):
    options.add_argument('--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(r"C:\chromedriver\chromedriver.exe", options=options)
    browser.get(f"https://www.nicb.org/vincheck")
    browser.set_page_load_timeout(10)

    elem = browser.find_element(By.CLASS_NAME, 'form-control')  # вставляем VIN в строку
    elem.send_keys(vin + Keys.RETURN)

    browser.find_element(By.ID, 'vincheck-recaptcha').find_element_by_tag_name('iframe').click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.NAME, "agree_terms"))).click()

    time.sleep(300)  # КАПЧА, не работает


def pars_site_autoastat(vin, options):
    # подключение прокси
    proxy_options = {
        'proxy': {
            'https': 'http://rD2jWa:mkHcvE@138.59.206.220:9409'
        }
    }
    try:  # запуск и проверка сайта на работоспособность
        browser = wier_webdriver.Chrome(r"C:\chromedriver\chromedriver.exe", options=options,
                                        seleniumwire_options=proxy_options)
        browser.get(f'https://autoastat.com/en/')
        browser.set_page_load_timeout(10)
    except Exception as ex:
        car_info_autoastat = {'info_autoastat': 'Сайт не работает',
                              'error_autoastat': str(ex)
                              }
        return car_info_autoastat

    try:
        # клик на авторизацию    
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                     'btn.btn-secondary.btn_mobile-unstyled'))).click()
        # авторизация на сайте   
        username = browser.find_element(By.ID, '_username')
        password = browser.find_element(By.ID, '_password')
        username.send_keys('tomaslex@mail.ru')
        password.send_keys('Lz_ZYB4-Xqfj4uP')

        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-primary.btn-sm'))).click()

        elem = browser.find_element(By.ID, 'search_lot_by_identifier_form_field')  # вставляем VIN в строку
        elem.send_keys(vin + Keys.RETURN)
    except Exception as ex:
        car_info_autoastat = {'info_autoastat': 'Сайт не работает',
                              'error_autoastat': str(ex)
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

            car_left_name = [item.get_text(strip=True).replace(' ', '_').replace(':', '') + '_autoastat'
                             for item in soup.find('div', class_='card-vehicle').find_all('dt')]

            car_mid_data = [item.get_text(strip=True).replace(' ', '_').replace(':', '')
                            for item in soup.find('div', class_='card full-height').find_all('dd')]

            car_mid_name = [item.get_text(strip=True).replace(' ', '_').replace(':', '') + '_autoastat'
                            for item in soup.find('div', class_='card full-height').find_all('dt')]

            car_right_data = [item.get_text(strip=True).replace(' ', '_').replace(':', '')
                              for item in soup.find('div', class_='card auction-card full-height').find_all('dd')]

            car_right_name = [item.get_text(strip=True).replace(' ', '_').replace(':', '') + '_autoastat'
                              for item in soup.find('div', class_='card auction-card full-height').find_all('dt')]

            car_info_autoastat = {**dict(zip(car_left_name, car_left_data)),
                                  **dict(zip(car_mid_name, car_mid_data)),
                                  **dict(zip(car_right_name, car_right_data))
                                  }

            return car_info_autoastat

        except Exception as ex:
            car_info_autoastat = {'info_autoastat': 'Нет информации',
                                  'error_autoastat': str(ex)
                                  }
            return car_info_autoastat

    return get_content(pagesource_autoastat)  # работает


def pars_site_reestr_zalogov(vin):
    browser = webdriver.Chrome(r"C:\chromedriver\chromedriver.exe")
    browser.get('https://www.reestr-zalogov.ru/search')

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT,
                                                                 "По информации о предмете залога"))).click()

    elem = browser.find_element(By.ID, 'vehicleProperty.vin')  # вставляем VIN в строку
    elem.send_keys(vin + Keys.RETURN)
    time.sleep(10)
    pagesource_reestr_zalogov = browser.page_source

    print(pagesource_reestr_zalogov)  # делает Игорь


def pars_site_vinfax(vin):
    browser = undetected_chromedriver.Chrome()
    browser.get(f'https://vinfax.site/index.php?q={vin}&lang=ru')
    pageSource_vinfax = browser.page_source

    soup = BeautifulSoup(pageSource_vinfax, "lxml")
    href = soup.find('div', class_='main__item').find('a').get('href')

    browser.get(f'https://vinfax.site{href}')

    time.sleep(5)  # делает Миша


def pars_site_gost(vin, options):
    try:
        browser = webdriver.Chrome(r"C:\chromedriver\chromedriver.exe", options=options)
        browser.get(f'https://easy.gost.ru/')
        browser.set_page_load_timeout(10)
    except Exception as ex:
        car_info_gost = {'info_gost': 'Сайт не работает',
                         'error_gost': str(ex)
                         }
        return car_info_gost

    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "btnFindVin")))
        elem = browser.find_element(By.ID, 'findVin')  # вставляем VIN в строку
        elem.send_keys(vin + Keys.RETURN)
    except Exception as ex:
        car_info_gost = {'info_gost': 'Сайт не работает',
                         'error_gost': str(ex)
                         }
        return car_info_gost

    time.sleep(2)
    pagesource_gost = browser.page_source
    browser.close()
    browser.quit()

    def get_content(source):
        try:
            soup = BeautifulSoup(source, "lxml")

            car_info_gost = dict(zip([
                'condition_gost', 'VIN_gost', 'revocable_company_gost', 'organizer_revocable_gost',
                'stamp', 'name_vehicle_gost', 'reasons_recall_gost', 'works_recommendations_gost'],
                [item for i, item in enumerate(soup.find('div', class_='div-revocamp').
                                               stripped_strings, 1) if i % 2 == 1]))
        except Exception as ex:
            car_info_gost = {'info_gost': 'Не найден среди отзывных кампаний',
                             'error_gost': str(ex)
                             }
            return car_info_gost

        return car_info_gost

    return get_content(pagesource_gost)  # работает


def pars_site_mvdgov(options):
    proxy_options = {
        'proxy': {
            'https': 'http://NiVprTat:GE5KUKUF@45.138.159.160:45150'
        }
    }
    browser = wier_webdriver.Chrome(r"C:\chromedriver\chromedriver.exe", options=options,
                                    seleniumwire_options=proxy_options)
    browser.get(f'https://www.reg.ru/web-tools/myip')
    browser.set_page_load_timeout(10)
    time.sleep(100)  # нужно белорусское прокси


def main():
    # подключение опций для браузера
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # включение фонового режима работы браузера
    options.add_argument("--mute-audio")  # отключение звука
    options.add_argument("""user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
                        (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36""")

    vin = '5YJ3E1EA1KF407691'

    # сохранение информации с сайтов в json-файлы
    with open(r"data_gibdd.json", 'w', encoding="utf-8") as outfile:
        json.dump(pars_site_gibdd(vin, options), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)

    with open(r"data_bidfax.json", 'w') as outfile:
        json.dump(pars_site_bidfax(vin), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)

    with open(r"data_gost.json", 'w') as outfile:
        json.dump(pars_site_gost(vin, options), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)

    with open(r"data_autoastat.json", 'w') as outfile:
        json.dump(pars_site_autoastat(vin, options), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()