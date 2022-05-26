import json
from .pars_site_bidfax import main_bidfax
# from .pars_site_fed_resource import main_fed_resource
from .pars_site_gost import main_gost
from .pars_site_autostat import main_autostat
# import .pars_site_costom_belarus
# from .pars_site_mvd_rb import main_mvd_rb # запускать только на сервере рб из-за включения впн
from .pars_site_gibbd_api import main_gibdd_api
from .pars_site_vinfax import main_vinfax
from threading import Thread
from selenium import webdriver


def get_options():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # включение фонового режима работы браузера
    options.add_argument("--mute-audio")  # отключение звука
    options.add_argument("""user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
                        (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36""")  # опции для для всех парсеров


def pars_without_reestor_rb(vin):
    # Thread(target=main_bidfax(vin)).start()
    #  Thread(target=main_autostat(vin)).start()
    # Thread(target=main_gost(vin)).start()
    # Thread(target=main_vinfax(vin)).start()
    # Thread(target=main_gibdd_api(vin)).start()
    # Thread(target=pars_site_costom_belarus.main_customs).start()
    # Thread(target=pars_site_fed_resource.main_fed_resource).start()
    # Thread(target=pars_site_mvd_rb.main_mvd_rb(vin)).start()  # запускать только на сервере рб из-за включения впн
    # return main_gibdd_api(vin)
    return main_gibdd_api(vin)
