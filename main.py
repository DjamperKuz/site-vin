"""Проект: сайт с поиском автомобильных номеров"""
import json
import pars_site_bidfax
import pars_site_gost
import pars_site_autostat
import pars_site_costom_belarus
import pars_site_gibdd_no_api
from selenium import webdriver


def get_browser(url, options=None):
    browser = webdriver.Chrome(r"C:\VIN\chromedriver\chromedriver.exe", options=options)
    browser.get(url)
    browser.set_page_load_timeout(10)
    return browser


def get_options():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # включение фонового режима работы браузера
    options.add_argument("--mute-audio")  # отключение звука
    options.add_argument("""user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
                        (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36""")  # опции для для всех парсеров


def save_json(dict_json, name_file):
    with open(f"data/{name_file}.json", 'w') as outfile:
        json.dump(dict_json, outfile, separators=(',', ': '), indent=4, ensure_ascii=False)


vin = 'WP0ZZZ97ZML189000'


def main():
    # pars_site_gibdd_no_api.main_gibdd()
    # pars_site_costom_belarus.main_customs()
    # pars_site_bidfax.main_bidfax()
    # pars_site_autostat.main_autostat()
    # pars_site_gost.main_gost()
    pass


if __name__ == "__main__":
    main()

