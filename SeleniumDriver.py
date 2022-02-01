from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


def init_webdriver():
    optiions = Options()
    optiions.headless = False
    optiions.add_argument("--window-size=1920,1080")
    service = Service("./chromedriver")
    service.creationflags = CREATE_NO_WINDOW
    driver: WebDriver = webdriver.Chrome(options=optiions, service=service)

    return driver