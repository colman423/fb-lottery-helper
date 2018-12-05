from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
# import re
# import os
import cookie_helper
from helper import *

# launch url
url_home = "http://www.facebook.com"
url_groups = "https://www.facebook.com/groups/"

# create a new Firefox session
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
driver = webdriver.Chrome('/Applications/chromedriver', options=chrome_options)

command = get_input("select an option by typing number\n1: login manually\n2: login by cookie file\n", ['1', '2'])
driver.implicitly_wait(500)
driver.get(url_home)

if command=='1':
    tmp = get_input("press any key after you logined.  ")
    print(tmp)
    if get_input("do you want to save login session as a cookie file? [y/n]  ", ['y', 'Y', 'n', 'N']) in ['y','Y']:
        cookie_helper.save(driver)
    
elif command=='2':
    cookie_helper.load(driver)
    driver.get(url_home)

driver.get(url_groups)
scrollBottom(driver)
a = driver.find_element_by_id('GroupDiscoverCard_membership').find_elements_by_class_name('_266w')
print(len(a))
for item in a:
    print(item.text)