import string
import random
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import T

def generate(length, lowercase_chars, uppercase_chars,digits, specialchars):
    password = ""
    choosed_characters = []

    if lowercase_chars:
        for c in list(string.ascii_lowercase):
            choosed_characters.append(c)
    if uppercase_chars:
        for c in list(string.ascii_uppercase):
            choosed_characters.append(c)
    if digits:
        for c in list(string.digits):
            choosed_characters.append(c)
    if specialchars:
        special_chars = "._-!@#$%&"
        for c in list(special_chars):
            choosed_characters.append(c)

    psw_in_list = random.choices(choosed_characters, k=length)
    for c in psw_in_list:
        password += c

    return password


lengths = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
layout = [   [sg.Text("Pasword length"), sg.Combo(lengths,readonly=True,size=(10,20),key="length")],
             [sg.Text("Lowercase letters"), sg.Checkbox("",key="lowercase")],
             [sg.Text("Uppercase letters"), sg.Checkbox("",key="uppercase")],
             [sg.Text("Numbers"), sg.Checkbox("",pad=(55,None),key="digits")],
             [sg.Text("Special chars"), sg.Checkbox("",pad=(29,None),enable_events=True,key="specialchars")],
             [sg.Button("Generate")],
             [sg.Text("Generated password: "), sg.InputText("",key="password")]
]   
window = sg.Window("Password Generator",layout,size=(380, 450),font=("Arial",11))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == "Generate":
        try:
            length = values["length"]
            lowercase_chars = values["lowercase"]
            uppercase_chars = values["uppercase"]
            digits = values["digits"]
            specialchars = values["specialchars"]

            psw = generate(length, lowercase_chars, uppercase_chars,digits, specialchars)

            window['password'].Update(psw)
        except Exception as err:
            sg.popup_error(err)