from vin_number.vinautocheck.vincheck.parsers.pars_settings import save_json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image
from anticaptchaofficial.imagecaptcha import *
import time


def parse_site_mvd_rb(vin):
    s = Service(executable_path="chromedriver/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
    options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,"
                         "image/avif,image/webp,image/apng,*/*; q=0.8,application/signed-exchange;v=b3;q=0.9")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(r"--user-data-dir=C:\Users\Igor-PC\Documents\carprice\vin_num\chromedriver\Profile 3")

    # options.add_argument("--headless") на сервере РБ убрать

    browser = webdriver.Chrome(service=s,
                               options=options)

    browser.get('https://www.mvd.gov.by/ru/service/6')
    browser.maximize_window()
    browser.execute_script("document.body.style.zoom='50%'")

    time.sleep(5)  # включается впн вручную, на сервере РБ убрать

    element = browser.find_element(By.ID, 'input_4')
    element.send_keys(vin)

    scrsht_element = browser.find_element(By.XPATH, """//div[@class="col-xs-9 ng-binding"]""")

    scrsht = f'data/captcha_{vin}.png'
    browser.get_screenshot_as_file(scrsht)
    img = Image.open(scrsht)

    size = scrsht_element.size

    left = 324
    top = 575
    right = left + size['width']
    bottom = top + size['height']

    img = img.crop((left, top, right, bottom))
    img.save(scrsht)

    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_case(True)
    solver.set_minLength(3)
    solver.set_maxLength(5)
    solver.set_key("87a89024d6e9e46f6d30f78ff4591d85")

    captcha_text = solver.solve_and_return_solution(scrsht)

    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    element_captcha = browser.find_element(By.ID, 'captcha')
    element_captcha.send_keys(captcha_text + Keys.RETURN)

    time.sleep(2)

    html_code = browser.page_source

    browser.close()
    browser.quit()

    return html_code


def get_mvd_info(code):
    soup = BeautifulSoup(code, "lxml")

    try:
        code_info = soup.find_all('b')

        return {"success": True,
                "data": {
                    'message': str(code_info).strip('[]<b>/'),
                    'er_message': None
                }}

    except Exception as ex:
        return {"success": True,
                "data": {
                    'message': None,
                    'er_message': ex
                }}


def main_mvd_rb(vin):
    save_json(get_mvd_info(parse_site_mvd_rb(vin)), 'data_mvd_rb')
