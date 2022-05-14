import json
import pars_site_bidfax
import pars_site_fed_resource
import pars_site_gost
import pars_site_autostat
import pars_site_costom_belarus
import pars_site_gibdd_no_api
import pars_site_vinfax
from threading import Thread
from selenium import webdriver
from sys import argv


def get_browser(url, options=None):
    browser = webdriver.Chrome(r"C:\VIN\chromedriver\chromedriver.exe", options=options)
    browser.get(url)
    browser.set_page_load_timeout(10)
    return browser


def get_options():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # ��������� �������� ������ ������ ��������
    options.add_argument("--mute-audio")  # ���������� �����
    options.add_argument("""user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
                        (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36""")  # ����� ��� ��� ���� ��������


def save_json(dict_json, name_file):
    with open(f"data/{name_file}.json", 'w', encoding="utf-8") as outfile:
        json.dump(dict_json, outfile, separators=(',', ': '), indent=4, ensure_ascii=False)


def pars_without_reestor_rb(vin):
    # Thread(target=pars_site_bidfax.main_bidfax).start()
    # Thread(target=pars_site_autostat.main_autostat).start()
    # Thread(target=pars_site_gibdd_no_api.main_gibdd).start()
    Thread(target=pars_site_gost.main_gost(vin)).start()
    # Thread(target=pars_site_costom_belarus.main_customs).start()
    # Thread(target=pars_site_vinfax.main_vinfax).start()
    # Thread(target=pars_site_fed_resource.main_fed_res).start()


vin = 'XWEGW413BG0000999'  # ����� ������ ��� �������
pars_without_reestor_rb(vin)

