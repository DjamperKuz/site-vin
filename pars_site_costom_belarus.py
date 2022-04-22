import time
import main
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pars_site_customs_belarus(vin, options):
    options.add_extension(r"C:\VIN\chromedriver\extension_2_5_1_0.crx")
    options.add_argument(r"--user-data-dir=C:\Users\tomas\AppData\Local\Google\Chrome\User Data\Default")
    browser = main.get_browser('https://www.customs.gov.by/baza-dannykh-vvezyennogo-avtotransporta/'
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


def main_customs():
    main.save_json(pars_site_customs_belarus(main.vin, main.get_options()), 'data_customs_belarus')


if __name__ == "main":
    main_customs()
