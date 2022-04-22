"""Проект: сайт с поиском автомобильных номеров"""
import time
import lxml
import json

import requests
import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver as wier_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.window import WindowTypes
from selenium.webdriver.support import expected_conditions as EC


def get_browser(url, options=None):
    browser = webdriver.Chrome(r"C:\VIN\chromedriver\chromedriver.exe", options=options)
    browser.get(url)
    browser.set_page_load_timeout(10)
    return browser


def pars_site_gibdd(vin, options):  # парсинг сайта ГИБДД, возвращает dict с информацией о машине
    try:  # запуск и проверка сайта на работоспособность
        browser = get_browser('https://xn--90adear.xn--p1ai/check/auto', options)
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
        try:
            soup_reg = soup.find('div', id='checkAutoHistory', class_='checkAutoSection')\
                                .find('ul', class_='fields-list vehicle')
            car_info_reg = dict(zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_') for item in
                                    soup_reg.find_all('span', class_='caption')],
                                    [item.get_text(strip=True).replace('\n', '') for item in
                                    soup_reg.find_all('span', class_='field')]))
        except Exception as ex:
            car_info_reg = {'info_reg': 'Нет информации',
                            'error_reg': str(ex)}

        # сбор информации о дтп
        try:
            text = 'В результате обработки запроса к АИУС ГИБДД записи о дорожно-транспортных происшествиях не найдены.'
            if text in soup.find('div', id='checkAutoContainer').get_text():
                car_info_dtp = {'info_dtp': text}
            else:
                car_info_dtp = {}

                soup_dtp = soup.find('div', id='checkAutoAiusdtp', class_='checkAutoSection')\
                                    .find('ul', class_='aiusdtp-list').find_all('ul', class_='fields-list aiusdtp-data')

                for i, object in enumerate(soup_dtp):
                    car_info_dtp[f'dtp_№_{i}'] = i
                    car_info_dtp = dict(
                        zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_') for item in
                             object.find_all('span', class_='caption')],
                            [item.get_text(strip=True).replace('\n', '') for item in
                             object.find_all('span', class_='field')]))
        except Exception as ex:
            car_info_dtp = {'info_dtp': 'Сервис не работает',
                            'error_dtp': str(ex)}

        # сбор информации о розыске
        try:
            text = 'По указанному VIN (номер кузова или шасси) не найдена информация о розыске транспортного средства.'
            if text in soup.find('div', id='checkAutoContainer').get_text():
                car_info_roz = {'info_roz': text}
            else:
                car_info_roz = {}

                soup_roz = soup.find('div', id='checkAutoWanted', class_='checkAutoSection')\
                    .find('ul', class_='wanted-list').find_all('ul', class_='fields-list wanted-data')

                # soup_roz_number = soup.find('div', id='checkAutoWanted',
                #                            class_='checkAutoSection').find_all('p', class_='ul-title')

                # for i, number in enumerate(soup_roz_number):
                #    car_info_roz[f'roz_№_{i}'] = number.get_text()

                for i, object in enumerate(soup_roz):
                    car_info_roz[f'roz_№_{i}'] = i
                    car_info_roz = dict(
                        zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_') for item in
                             object.find_all('span', class_='caption')],
                            [item.get_text(strip=True).replace('\n', '') for item in
                             object.find_all('span', class_='field')]))
        except Exception as ex:
            car_info_roz = {'info_roz': 'Сервис не работает',
                            'error_roz': str(ex)}

        # сбор информации о наложенных ограничениях
        try:
            text = '''По указанному VIN (номер кузова или шасси) не найдена информация о наложении ограничений на 
            регистрационные действия с транспортным средством.'''
            if text in soup.find('div', id='checkAutoContainer').get_text():
                car_info_ogran = {'info_ogran': text}
            else:
                car_info_ogran = {}

                soup_ogran = soup.find('div', id='checkAutoRestricted', class_='checkAutoSection')\
                    .find('ul', class_='restricted-list').find_all('ul', class_='fields-list restrict-data')

                for i, object in enumerate(soup_ogran):
                    car_info_ogran[f'ogran_№_{i}'] = i
                    car_info_ogran = dict(
                        zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_') for item in
                             object.find_all('span', class_='caption')],
                            [item.get_text(strip=True).replace('\n', '') for item in
                             object.find_all('span', class_='field')]))

        except Exception as ex:
            car_info_ogran = {'info_ogran': 'Сервис не работает',
                              'error_ogran': str(ex)}

        return dict(**car_info_reg, **car_info_dtp, **car_info_roz, **car_info_ogran)

    return get_content(pagesource_gibdd)  # работает, добавить периоды владения


def site_gibdd_api(vin):
    checks = {
        "history": "history",
        "dtp": "aiusdtp",
        "wanted": "wanted",
        "restrict": "restricted",
        "diagnostic": "diagnostic"
    }
    for link in list(checks.keys()):
        url = f"https://xn--blafk4ade.xn--90adear.xn--plai/proxy/check/auto/{link}"

        data = {
            "vin": vin,
            "checkType": checks[link]
        }
        try:
            r = requests.post(url, data=data)
            print(json.loads(r.text))
        except Exception as ex:
            print(ex)


def pars_site_bidfax(vin):  # парсинг сайта bidfax, возвращает dict с информацией о машине
    try:  # запуск и проверка сайта на работоспособность
        browser = get_browser('https://bidfax.info/')
    except Exception as ex:
        car_info_bidfax = {
            'success': 'False',
            'info_bidfax': 'Сайт не работает'
        }
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
        car_info_bidfax = {
            'success': 'False',
            'info_bidfax': 'Нет информации о машине'
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
        car_info = dict(zip([
            'lot_number', 'date_of_sale', 'year_of_release', 'VIN',
            'status', 'engine', 'mileage',
            'seller', 'documents', 'place_of_sale', 'primary_damage',
            'secondary_damage',
            'est._retail_value_dollars', 'repair_price_dollars', 'transmission',
            'color', 'drive', 'fuel', 'keys', 'notes'],
            [item.get_text(strip=True) for item in car_info.find_all("span", class_="blackfont")]))
        try:
            car_info['auction_bidfax'] = soup.find('span', class_='copart').get_text(strip=True)
        except:
            car_info['auction_bidfax'] = soup.find('span', class_='iaai').get_text(strip=True)

        # сбор фотографий
        photo = ['https://bidfax.info/' + item.get('src') for item in car_photo.find_all('img')]
        for i in range(1, len(photo) + 1):
            car_info[f'car_photo_number_{i}'] = photo[i - 1]

        car_info_bidfax = {
            'success': 'True',
            **car_info
        }

        return car_info_bidfax

    return get_content(pagesource_bidfax)  # работает


def pars_site_nicb(vin, options):
    browser = get_browser('https://www.nicb.org/vincheck', options)

    elem = browser.find_element(By.CLASS_NAME, 'form-control')  # вставляем VIN в строку
    elem.send_keys(vin + Keys.RETURN)

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.NAME, "agree_terms"))).click()

    time.sleep(30)  # КАПЧА, не работает


def pars_site_autoastat(vin, options):
    # подключение прокси
    proxy_options = {
        'proxy': {
            'https': 'http://rD2jWa:mkHcvE@138.59.206.220:9409'
        }
    }
    try:  # запуск и проверка сайта на работоспособность
        browser = wier_webdriver.Chrome(r"C:\VIN\chromedriver\chromedriver.exe", options=options,
                                        seleniumwire_options=proxy_options)
        browser.get(f'https://autoastat.com/en/')
        browser.set_page_load_timeout(10)
    except Exception as ex:
        car_info_autoastat = {
            'success': 'False',
            'info_autoastat': 'Сайт не работает'
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


def pars_site_reestr_zalogov(vin):
    browser = webdriver.Chrome(r"C:\VIN\chromedriver\chromedriver.exe")
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
        browser = get_browser('https://easy.gost.ru/', options)
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


def pars_site_customs_belarus(vin, options):
    options.add_extension(r"C:\VIN\chromedriver\extension_2_5_1_0.crx")
    options.add_argument(r"--user-data-dir=C:\Users\tomas\AppData\Local\Google\Chrome\User Data\Default")
    browser = get_browser('https://www.customs.gov.by/baza-dannykh-vvezyennogo-avtotransporta/'
                          'index.php?sphrase_id=157722', options=options)
    time.sleep(20)

    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "filter")))
        elem = browser.find_elements(By.NAME, 'query')
        for item in range(len(elem)):
            elem[item].send_keys(vin + Keys.RETURN)
            time.sleep(5)
    except:
        car_info_customs = {
            'success': 'False',
            'info_customs': 'Сайт не работает'
        }
        return car_info_customs

    pagesource_customs = browser.page_source  # сохранение html кода страницы
    browser.close()
    browser.quit()

    def get_content(source):
        soup = BeautifulSoup(source, "lxml")

        text = "Ничего не найдено"
        try:
            if text in soup.find('div', class_='db_table1').get_text():
                check_table1 = True
                car_info_table1 = {}
            else:
                check_table1 = False
                soup_table1 = soup.find('div', class_='db_table1')
                car_info_table1 = dict(zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_')
                                for item in soup_table1.find_all('th')],
                                [item.get_text(strip=True).replace('\n', '') for item in soup_table1.find_all('td')]))

            if text in soup.find('div', class_='db_table2').get_text():
                check_table2 = True
                car_info_table2 = {}
            else:
                check_table2 = False
                soup_table2 = soup.find('div', class_='db_table2')
                car_info_table2 = dict(zip([item.get_text(strip=True).replace('\n', '').replace(' ', '_')
                                for item in soup_table2.find_all('th')],
                                [item.get_text(strip=True).replace('\n', '') for item in soup_table2.find_all('td')]))

            if (check_table1 == True) and (check_table2 == True):
                car_info_customs = {
                    'success': 'True',
                    'info_customs': 'Ничего не найдено'
                }
            else:
                car_info_customs = {
                    'success': 'True',
                    **car_info_table1,
                    **car_info_table2
                }
        except Exception as ex:
            car_info_customs = {
                'success': 'False',
                'info_customs': 'Сайт не работает'
            }

        return car_info_customs

    return get_content(pagesource_customs)

def main():
    # подключение опций для браузера
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # включение фонового режима работы браузера
    options.add_argument("--mute-audio")  # отключение звука
    options.add_argument("""user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
                        (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36""")

    vin = 'WP0ZZZ97ZML189042'
    '''
    with open(r"data/data_customs_belarus.json", 'w', encoding="utf-8") as outfile:
        json.dump(pars_site_customs_belarus(vin, options), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)

    with open(r"data/data_gibdd.json", 'w', encoding="utf-8") as outfile:
        json.dump(pars_site_gibdd(vin, options), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)
    
    with open(r"data/data_bidfax.json", 'w') as outfile:
        json.dump(pars_site_bidfax(vin), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)
    '''
    with open(r"data/data_gost.json", 'w') as outfile:
        json.dump(pars_site_gost(vin, options), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)

    with open(r"data/data_autoastat.json", 'w') as outfile:
        json.dump(pars_site_autoastat(vin, options), outfile, separators=(',', ': '), indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()

