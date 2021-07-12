import json
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
import requests
import PySimpleGUI as sg


def country_info(json_response):
    infos = []
    
    #name
    name = json_response['name']
    infos.append(name)

    #capital
    capital = f"Country's capital: {json_response['capital']}"
    infos.append(capital)

    #language
    languages = f"Langueges: {json_response['languages']}"
    infos.append(languages)

    #population
    population = f"Population: {json_response['population']} people"
    infos.append(population)

    #calling code
    call_code = f"Country's telephone prefix: +{json_response['callingCodes'][0]}"
    infos.append(call_code)

    #borders
    borders = f"Borders: {json_response['borders']}"
    infos.append(borders)

    #currencies
    currencies = f"Currencies: {json_response['currencies'][0]}"
    infos.append(currencies)

    #main domain name
    domain = f"Contry's top level domain: {json_response['topLevelDomain'][0]}"
    infos.append(domain)

    return infos


#USER INTERFACE

layout = [
    [sg.Text("Write the name of a country to learn some new informations about it!")],
    [sg.InputText(key="country")], [sg.Button("Search")],
    [sg.Multiline(key="output", size=(65, 8))],
    [sg.Button("Quit research")]
] 

window = sg.Window("Countries main informations", layout=layout)

while True:
    event, values = window.read()

    if (event == sg.WINDOW_CLOSED) or (event == "Quit research"):
        break
    
    elif event == "Search":
        country = values['country']  #content of the input form

        if country != None:
            window['output'].update("", append=False)

        endpoint = f"https://restcountries.eu/rest/v2/name/{country}?fullText=True"
        response = requests.get(endpoint)
        status_code = response.status_code

        if status_code == 200:
            infos = []
            json_response = response.json()[0] #the [0] is a fix for a json response issue
            for infos in country_info(json_response):
                line = f"{infos}\n"
                window['output'].update(line, append=True)
        else:
            sg.PopupAnnoying("SOMETHING WRONG WITH THE REQUEST, MAYBE TRY TO WRITE THE CORRECT COUNTRY NAME.")


