from os import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



# Stay Logged In
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=/tmp/tarun")

# Tell Chrome that you are not a robot
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')







def formFill(path, userInput):
    browser.find_element_by_xpath(path).send_keys(userInput)


async def checkProduct(link):
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(link)
    elem = browser.find_element_by_class_name('container_3LC03')
    if elem == "Available to ship":
        browser.find_element_by_id("test").click()
        time.sleep(3)
        print("Added to Cart!")
        return 'https://www.bestbuy.ca/checkout/?qit=1#/en-ca/shipping/ON/M1H%201L9'
    else:
        return 'Not available'

