from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



PATH = "C:\Program Files (x86)\chromedriver"
driver = webdriver.Chrome(PATH) #cio che gestisce le interazioni con l'web

USER = str(input("inserisci lo username: "))
PSW = str(input("inserisci la password: "))

time.sleep(5)

driver.get("https://aldini-valeriani-bo.registroelettronico.com/mastercom/")
driver.implicitly_wait(5)

utente = driver.find_element_by_name("user")
utente.send_keys(USER)
utente.send_keys(Keys.RETURN)

time.sleep(3)

psw = driver.find_element_by_name("password_user")
psw.send_keys(PSW)
psw.send_keys(Keys.RETURN)

