from selenium import webdriver
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locadora.settings.development')

django.setup()

def before_all(context):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    context.browser = webdriver.Chrome("/usr/local/share/chromedriver", chrome_options=chrome_options)
    context.browser.maximize_window()
    context.browser.implicitly_wait(20)

def after_all(context):
    context.browser.quit()
