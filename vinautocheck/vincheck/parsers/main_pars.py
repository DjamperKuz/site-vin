import json
# import pars_site_bidfax
# import pars_site_fed_resource
from .pars_site_gost import main_gost
from .pars_site_autostat import main_autostat
# import pars_site_costom_belarus
# import pars_site_gibdd_no_api
# import pars_site_vinfax
from threading import Thread
from selenium import webdriver


def get_options():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # включение фонового режима работы браузера
    options.add_argument("--mute-audio")  # отключение звука
    options.add_argument("""user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
                        (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36""")  # опции для для всех парсеров


def pars_without_reestor_rb(vin):
    print('pars_without_reestor_rb')
    # Thread(target=pars_site_bidfax.main_bidfax).start()
    Thread(target=main_autostat(vin)).start()
    # Thread(target=pars_site_gibdd_no_api.main_gibdd).start()
    Thread(target=main_gost(vin)).start()
    # Thread(target=pars_site_costom_belarus.main_customs).start()
    # Thread(target=pars_site_vinfax.main_vinfax).start()
    # Thread(target=pars_site_fed_resource.main_fed_res).start()

