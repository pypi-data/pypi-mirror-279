from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

option = ChromeOptions()
# option.add_argument('--user-data-dir=C:\\Users\\hangkai.hu\\AppData\\Local\\Google\\Chrome\\User Data')  # 设置成用户自己的数据目录

option.add_experimental_option("excludeSwitches", ["enable-automation"])
path = Service('chromedriver.exe')
driver = webdriver.Chrome(options=option, service=path)
# driver = webdriver.Chrome()

driver.get('https://di.radar-ev.com/portrait/home', headers={})
print("")