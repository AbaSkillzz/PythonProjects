from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



PATH = "C:\Program Files (x86)\chromedriver"
driver = webdriver.Chrome(PATH) #cio che gestisce le interazioni con l'web

driver.get("https://aldini-valeriani-bo.registroelettronico.com/mastercom/")
driver.implicitly_wait(5)

utente = driver.find_element_by_name("user")
utente.send_keys("529208")
utente.send_keys(Keys.RETURN)

time.sleep(3)

psw = driver.find_element_by_name("password_user")
psw.send_keys("ababil2005")
psw.send_keys(Keys.RETURN)

