import urllib.request
from bs4 import BeautifulSoup as bs


searching_link = input("Link >>> ")
html = urllib.request.urlopen(searching_link)  #html da controllare

soup = bs(html, "html.parser")  

tag_to_search = soup("a") #cerco tutti i tag ad esempio --> a(anchor)

for tag in tag_to_search: 
    print(tag.get("href"))  #e dai vari tag link, cerco i link(indirizzi a cui portano)



