import time
import main
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pars_site_gibdd(vin):  # парсинг сайта ГИБДД, возвращает dict с информацией о машине
    options = main.webdriver.ChromeOptions()
    options.add_argument("--mute-audio")  # отключение звука
    # options.add_argument("--headless")  # включение фонового режима работы браузера
    try:  # запуск и проверка сайта на работоспособность
        browser = main.get_browser('https://xn--90adear.xn--p1ai/check/auto', options)
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
            car_info_reg = {'info_reg': 'Нет информации о регистрации ТС',
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
            text = "По указанному VIN (номер кузова или шасси) не найдена информация" \
                   " о наложении ограничений на регистрационные действия с транспортным средством."
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


def main_gibdd():
    main.save_json(pars_site_gibdd(main.vin), 'data_gibdd_no_api')


if __name__ == "__main__":
    main_gibdd()
