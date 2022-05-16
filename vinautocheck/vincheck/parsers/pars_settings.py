import json
from selenium import webdriver


def save_json(dict_json, name_file):
    with open(f"data/{name_file}.json", 'w', encoding="utf-8") as outfile:
        json.dump(dict_json, outfile, separators=(',', ': '), indent=4, ensure_ascii=False)


def get_browser(url, options=None):
    # browser = webdriver.Chrome(r"C:/VIN/vinautocheck/vincheck/parsers/chromedriver/chromedriver.exe", options=options)
    browser = webdriver.Chrome(r"chromedriver/chromedriver.exe", options=options)
    browser.get(url)
    browser.set_page_load_timeout(10)
    return browser
