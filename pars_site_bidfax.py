import time
import main
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pars_site_bidfax(vin):  # парсинг сайта bidfax, возвращает dict с информацией о машине
    try:  # запуск и проверка сайта на работоспособность
        browser = main.get_browser('https://bidfax.info/')
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


def main_bidfax():
    main.save_json(pars_site_bidfax(main.vin), 'data_bidfax')


if __name__ == "main":
    main_bidfax()
