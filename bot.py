from os import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# profile = FirefoxProfile("/home/tahbib/Documents/Projects/Discord_Bot")
# options = Options()
# #options.headless = True
# options.add_argument("--headless")
# browser = webdriver.Firefox(firefox_profile=profile,options=options)

# link = 'https://www.bestbuy.ca/en-ca/product/garmin-forerunner-245-30mm-gps-watch-with-heart-rate-monitor-large-slate-grey/13531661'
# browser.get(link)
#assert 'BestBuy' in browser.title

#elem = browser.find_element_by_name('p')  # Find the search box#
#elem.send_keys('seleniumhq' + Keys.RETURN)

# Stay Logged In
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=/tmp/tarun")

# Tell Chrome that you are not a robot
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')




link = 'https://www.bestbuy.ca/en-ca/product/sony-in-ear-noise-cancelling-truly-wireless-headphones-wf-1000xm3-silver/13794647?icmp=Recos_3across_tp_sllng_prdcts&referrer=PLP_Reco'

browser = webdriver.Chrome(options=chrome_options)
browser.get(link)

def formFill(path, userInput):
    browser.find_element_by_xpath(path).send_keys(userInput)


def checkProduct(link):
    

for x in range(10):
    elem = browser.find_element_by_class_name('container_3LC03')
    print(elem.text)
    if elem.text == "Available to ship":
            browser.find_element_by_id("test").click()
            time.sleep(3)
            print("Added to Cart!")
            browser.get('https://www.bestbuy.ca/checkout/?qit=1#/en-ca/shipping/ON/M1H%201L9')
            
            #form filling
            browser.find_element_by_xpath('//*[@id="email"]').send_keys("to2001628@gmail.com")
            time.sleep(1)

            browser.find_element_by_xpath('//*[@id="firstName"]').send_keys("Tahbib")
            time.sleep(1.5)

            browser.find_element_by_xpath('//*[@id="lastName"]').send_keys("Osman")
            time.sleep(1)

            browser.find_element_by_xpath('//*[@id="addressLine"]').send_keys("72 Gaiety Drive" + Keys.ESCAPE)
            time.sleep(1.5)

            browser.find_element_by_xpath('//*[@id="regionCode"]/option[10]').click()
            time.sleep(1)

            formFill('//*[@id="city"]','Scarborough')

            formFill('//*[@id="postalCode"]','M1H 1C1')

            formFill('//*[@id="phone"]',('4373459904'))

            browser.find_element_by_xpath('//*[@id="posElement"]/section/section[1]/button/span').click()
            time.sleep(2)
            formFill('//*[@id="shownCardNumber"]', '4510157541123348')
            time.sleep(2)

            browser.find_element_by_xpath('//*[@id="expirationMonth"]/option[@value="11"]').click()
            time.sleep(2)

            browser.find_element_by_xpath('//*[@id="expirationYear"]/option[@value="2024"]').click()
            time.sleep(3)

            formFill('//*[@id="cvv"]','123')
            time.sleep(1)

            #browser.find_element_by_xpath('//*[@id="posElement"]/section/section[1]/button').click()

            time.sleep(3)

            browser.quit()

    time.sleep(2)
    browser.refresh()
