""" Method(s) for custom selenium webdriver"""

from subprocess import CREATE_NO_WINDOW
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


def start_webdriver() -> WebDriver:
    """Starts custom Chrome webdriver and returns it"""
    options = Options()
    options.add_argument("--window-size=1920,1080")
    service = Service()
    service.creationflags = CREATE_NO_WINDOW
    driver: WebDriver = Chrome(options=options, service=service)

    return driver
