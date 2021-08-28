from tkinter.constants import DISABLED
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Window, execute_py_get_interpreter
from pynput import keyboard
import pynput
from pynput.keyboard import Key, Listener
import threading
import time
import os
import signal


#WINDOW, UI
def create_test_window():
    text_frame_layout = [ [sg.Multiline(disabled=True, no_scrollbar=True, size=(300, 30), key="text")] ]
    input_frame_layout = [ [sg.Input(size=(500,200), background_color="white", key="input", enable_events=True)] ]
    layout = [  [sg.Text("Set test timer:", background_color="#1158f2"), sg.Combo(values=["Slow", "Normal", "Fast", "Very Fast"], size=(6,None), readonly=True, key="settimer"), sg.Text("Counter", background_color="#1158f2", key="counter"), sg.Button("start", button_color="green", border_width=0, enable_events=True, pad=(20, None))],
                [sg.Frame("Text", layout=text_frame_layout, background_color="#1158f2", border_width=0.5, relief="solid")],
                [sg.Frame("Input", layout=input_frame_layout, background_color="#1158f2", border_width=0.5, relief="solid", key="input_frame") ]
    ]
    return sg.Window("Typing Speed Test", layout=layout, size=(750, 550), background_color="#1158f2")


#FUNCTIONALITIES, PROCESSING
def score(seconds):
    paragraph = open("path_to_file_with_text_to_copy", "r")
    user_text = open("path_to_file_where_save_user_inputs", "r")
    
    paragraph_content = paragraph.read()
    user_content = user_text.read()

    paragraph_content_list = list(str(paragraph_content))
    user_content_list = list(str(user_content))
    
    #error counting
    errors = 0
    for char in range(len(user_content_list)):
        if user_content_list[char] != paragraph_content_list[char]:
            errors += 1

    #characters and keystrokes counting 
    total_keystrokes = 0
    for c in user_content:
        total_keystrokes += 1

    #net WPM calculation
    minutes = seconds/60
    valid_keystrokes = total_keystrokes - errors
    total_words = valid_keystrokes // 5
    net_wpm = total_words // minutes

    #accurancy calculation
    accurancy_value = (valid_keystrokes/total_keystrokes) * 100
  
    score_win_layout = [[sg.Text(f"Time: {round(minutes,3)} (min)")],
                        [sg.Text(f"Keystrokes:{total_keystrokes}"), sg.Text(f"Valid Keystrokes:{valid_keystrokes}", text_color="green"), sg.Text(f"Errors:{errors}", text_color="red")],
                        [sg.Text(f"WPM:{net_wpm}"), sg.Text(f"Accurancy: {round(accurancy_value,1)}%")] ]
                        
    return sg.Window("Score", score_win_layout)
    
def counter():
    timer_at = value["settimer"]
    if timer_at == "Slow":
        set_time = 120
    elif timer_at == "Normal":
        set_time = 60
    elif timer_at == "Fast":
        set_time = 30
    elif timer_at == "Very Fast":
        set_time = 10

    test_time = set_time

    while set_time > 0:
        time.sleep(1)
        set_time -= 1
        window["counter"].Update(f"0:{set_time}")

    with open("path_to_file_where_save_user_inputs", "a") as f:
            f.write(value["input"])
    window["input"].Update("")
    window["counter"].Update("Counter")
    window["input"].Update(disabled=True)
    window.close()

    score_win = score(test_time)
    while True:
        event2, value2 = score_win.read()
        if event2 == sg.WIN_CLOSED:
            break
            
counter_thread = threading.Thread(target=counter, args=())

#MAIN LOOP
window  = create_test_window()
while True:
    event, value = window.read()
    if event == sg.WIN_CLOSED:
        os.kill(os.getpid(), signal.SIGTERM)

    elif event == "start":
        time.sleep(1)
        try:
            #restoring the user's input file
            with open("path_to_file_where_save_user_inputs", "w") as inp_file:
                inp_file.write("")
            paragraph = open("path_to_file_with_text_to_copy", "r")
            window["text"].Update(paragraph.read())
            window["input"].Update("")
            window["input_frame"].Update("Write to start the the test")
            
            if not counter_thread.is_alive(): 
                counter_thread.start()
        
        except Exception as err:
            sg.popup_error(err)
    
