from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re 
# Replace below path with the absolute path
# to chromedriver in your computer
driver = webdriver.Chrome('/Users/mannumalhotra/Downloads/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)

path = '//*[@id="main"]/div[2]/div/div/div[3]/div[last()]/div/div/div/div/span'
delay = 1


#Focus on the group!
group_name = '"Headless"'
x_arg = '//span[contains(@title,' + group_name + ')]'
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
group_title.click()

#Start getting the messages

def isUnwanted(body):
    urls = re.findall('[h|H]ttp[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
    for url in urls:
        print url, "https://www.oyewiki.com" not in url
        if "https://www.oyewiki.com" not in url:
            return True
    return False


def removeUser():
    pass

while True:    
    body = wait.until(EC.presence_of_element_located((By.XPATH, path))).text
    print body
    if isUnwanted(body):
        removeUser()
        print("Unwanted found!")
    time.sleep(delay)