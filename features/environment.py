from selenium import webdriver
import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locadora.settings.development')

django.setup()

def before_all(context):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option("detach", True)
    context.browser = webdriver.Chrome("/usr/local/share/chromedriver", chrome_options=chrome_options)
    context.browser.maximize_window()
    context.browser.implicitly_wait(50)

# def after_all(context):
#     context.browser.get('http://127.0.0.1:8000/accounts/logout')
#     context.browser.quit()