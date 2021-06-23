from cryptography.fernet import Fernet
import PySimpleGUI as sg



#ENCRYPTION FUNCTION
def criptazione(plain_text_file, cipher_destination):
    #generating encryption and decryption key
    key = Fernet.generate_key()
    #creating a fernet object, it will allow to encrypt and decrypt
    fernet = Fernet(key)
    #read the plain text content to encrypt
    with open(plain_text_file, "rb") as file:
        data_to_encrypt = file.read() 
    #encryption
    encripted_data = fernet.encrypt(data_to_encrypt)
    #store the encrypted data in the file(substituting the encrypted data with the plain text)
    with open(cipher_destination, "wb") as cipher:
        cipher.write(encripted_data)

    sg.popup_get_text(f"Save this key      {key}     for the decryption(copy the code between the quotation marks and save it) ", size=(100, 2), default_text=key)


#DECRYPTION FUNCTION
def decriptazione(cipher_file, chiave):
    fernet = Fernet(chiave)
    #read the encrypted file data
    with open(cipher_file, "rb") as file:
        data_to_decrypt = file.read()
    #decryption
    decrypted_data = fernet.decrypt(data_to_decrypt)
    #store the decrypted data in the file(substitution of data)
    with open(cipher_file, "wb") as plain_text:
        plain_text.write(decrypted_data)
    
    sg.popup("DECRYPTION DONE. GO TO CHECK THE FILE GIVEN BY YOU, NOW IT SHOULD BE DECRYPTED.")
   


#USER INTERFACE

#window's structures
layout = [
    [sg.Text("Write 'criptazione' if you want to encript a file \nor write 'decriptazione' if you want to decript a file")],
    [sg.InputText(key="choice")],
    [sg.Button("OK"), sg.Button("QUIT")]
]

encryption_layout = [
    [sg.Text("Give the path of the file to encrypt: ")],
    [sg.InputText(key="file_to_encrypt"), sg.FileBrowse()],
    [sg.Text("Give the path of a DESTINATION to store the encryption: ")],
    [sg.InputText(key="encryption_destination"), sg.FileBrowse()],
    [sg.Button("OK"), sg.Button("QUIT")]
]

decryption_layout = [
    [sg.Text("Give the path of the file to decrypt: ")],
    [sg.InputText(key="file_to_decrypt"), sg.FileBrowse()],
    [sg.Text("Paste here the key by which you have encrypted the file:")],
    [sg.InputText(key="key")],
    [sg.Button("OK"), sg.Button("QUIT")]
]

#main window creation
window = sg.Window("Cryptography", layout=layout)

#event loop, the core part of window's functions
while True:
    event, values = window.read()

    if event==sg.WINDOW_CLOSED or event=="QUIT":
        break

    else:
        choice = values["choice"]  #before closing the window, getting the choice
        window.close()

        if choice == "criptazione":
            encryption_window = sg.Window("Encryption", encryption_layout)
            #event loop
            while True:
                event, values = encryption_window.read()
                if event==sg.WINDOW_CLOSED or event=="QUIT":
                    break
                
                elif event == "OK":
                    file_to_encrypt = values["file_to_encrypt"] 
                    destionation = values["encryption_destination"]

                    encryption_window.close()

                    try:
                        criptazione(file_to_encrypt, destionation)
                    except:
                        sg.popup("SOME ERROR OCCURED WITH THE ENCRYPTION")

        elif choice == "decriptazione":
            decryption_window = sg.Window("Decryption", decryption_layout)
            #event loop
            while True:
                event, values = decryption_window.read()
                if event==sg.WINDOW_CLOSED or event=="QUIT":
                    break

                file_to_decrypt = values["file_to_decrypt"]
                key = values["key"]

                try:
                    decriptazione(file_to_decrypt, key)
                except:
                    sg.popup("SOME ERROR OCCURED WITH THE DECRYPTION, MAYBE YOU ENTERED THE WRONG KEY!")

        else:
            sg.popup_auto_close("YOU WROTE SOMETHING WRONG!!! CHOOSE 'criptazione' or 'decriptazione'\n(self-closing popup)")