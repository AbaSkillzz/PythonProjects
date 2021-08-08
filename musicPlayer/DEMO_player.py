from tkinter import EXCEPTION, font
from PySimpleGUI.PySimpleGUI import Window, execute_py_get_interpreter
import PySimpleGUI as pysg
import pygame
import time
import os
import signal
from pathlib import Path
import threading
import random



#---FUNCTIONS---------------------------------------------------------------------------------------------------------------------
def locator(musics_dir, file_filter):
    files = []
    if os.path.isdir(musics_dir):
        if file_filter:
            no_filtered_files = os.listdir(musics_dir)
            for f in no_filtered_files:
                if (Path(f).suffix=='.mp3') or (Path(f).suffix)=='.wav':
                    files.append(f)     
        elif file_filter == False:
            files = os.listdir(musics_dir)

        return files
    else:
        return "INVALID DIRECTORY PATH!"


def play_music(dir_path, song):
    try: 
        pygame.mixer.music.load(f'{dir_path}/{song}')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        return("SONG FINISHED!")

    except Exception as err:
        return err
    


#---MAIN, USER INTERFACE----------------------------------------------------------------------------------------------------------
pygame.mixer.init()

music_lenght = 0
music_controller_layout = [ 
            [pysg.Text('',key='song_status',font=('arial',7),size=(30,1),background_color='#1a1a26')],
            [pysg.Text('',key='song_name',size=(46,1),font=('arial',8),background_color='#1a1a26',text_color='#d712ff')],
            [pysg.Button('start',border_width=0,size=(3,1),button_color='#1a1a26',mouseover_colors='#d712ff'), pysg.Button('random',border_width=0,size=(4,1),button_color='#1a1a26',mouseover_colors='#d712ff'),pysg.Button('pause',border_width=0,size=(3,1),button_color='#1a1a26',mouseover_colors='#d712ff'), pysg.Button('unpause',border_width=0,size=(4,1),button_color='#1a1a26',mouseover_colors='#d712ff'), pysg.Button('stop',border_width=0,size=(4,1),button_color='#1a1a26',mouseover_colors='#d712ff')],
            [pysg.Text('vol.',pad=(10,10),background_color='#1a1a26'), pysg.Slider(range=(0,10),default_value=5,resolution=1,orientation='h',enable_events=True,key='volume',background_color='#1a1a26',trough_color='#d712ff')] ]
panel_layout = [ 
            [pysg.Text('Click "Search files" to list the files of the folder.',font=('Arial',8),text_color='yellow',background_color='#1a1a26')],
            [pysg.Text('NOTICE: Only .mp3 and .wav files to listen music!',font=('Arial',8),text_color='yellow',background_color='#1a1a26')],
            [pysg.Checkbox('Filter only acceptable music files',key="filter_checkbox",font=('Arial',12),background_color='#1a1a26')], 
            [pysg.Button('Search files',border_width=0,size=(15,1),button_color='#1a1a26',mouseover_colors='#d712ff')],
            [pysg.Frame('',layout=music_controller_layout,pad=(6,65),background_color='#1a1a26',border_width=0.1)] 
               ]
files = []
layout = [
    [pysg.Text("Music player",font=('Arial',22),background_color='#1a1a26',text_color='#d712ff')],
    [pysg.Text('Choose the folder with your music files:',font=('Arial',10),background_color='#1a1a26'), pysg.Input(key='dir_path'), pysg.FolderBrowse(size=(14,0),button_color='#1a1a26')],
    [pysg.Listbox(files,size=(65,25),key='file_list',select_mode='LISTBOX_SELECT_MODE_SINGLE',enable_events=True,background_color='#1a1a26',text_color='white'), pysg.Column(panel_layout,size=(600,300),background_color='#1a1a26')],
         ]   

window = pysg.Window("Music Player",layout, size=(820, 430),background_color='#1a1a26')

while True:
    event, values = window.read()
    if event == pysg.WIN_CLOSED:
        os.kill(os.getpid(), signal.SIGTERM)  #kills all the processes(included the song thread)
        break
        
    elif event == 'Search files':
        dir_path = values['dir_path']
        file_filter = values['filter_checkbox']
        locator_response = locator(dir_path, file_filter)

        if locator_response == "INVALID DIRECTORY PATH!":
            pysg.popup_error(locator_response)
        else:
            window['file_list'].update(locator_response)
        
    elif event == 'start':
        try:
            dir_path = values['dir_path']
            song_file = values['file_list'][0]
            song_name = Path(song_file).stem
            music_thread = threading.Thread(target=play_music, args=(dir_path, song_file,))
            music_thread.start()
            window['song_name'].update(song_name)
            window['song_status'].update('Playing:')
        except Exception as err:
            pysg.popup_error(err)

    elif event == 'pause':
        try:
            pygame.mixer.music.pause()
            window['song_status'].update('Paused:')
        except Exception as err:
            pysg.popup_error(err)

    elif event == 'unpause':
        try:
            pygame.mixer.music.unpause()
            window['song_status'].update('Playing:')
        except Exception as err:
            pysg.popup_error(err)

    elif event == 'stop':
        try:
            pygame.mixer.music.stop()
            window['song_status'].update('')
            window['song_name'].update('')
        except Exception as err:
            pysg.popup_error(err)

    elif event == 'volume':
        try:
            pygame.mixer.music.set_volume((values['volume'])/10)
        except Exception as err:
            pysg.popup_error(err)

    elif event == 'random':
        dir_path = values['dir_path']
        file_filter = True
        locator_response = locator(dir_path, file_filter)
        if locator_response == "INVALID DIRECTORY PATH!":
            pysg.popup_error(locator_response)
        else:
            if len(locator_response) == 0: #if the list is empty(no acceptable file)
                pysg.popup_error('Did not find any proper file in this folder!')
            else:
                try:
                    file_to_play = random.choice(locator_response)
                    dir_path = values['dir_path']
                    song_name = Path(file_to_play).stem
                    music_thread = threading.Thread(target=play_music, args=(dir_path, file_to_play,))
                    music_thread.start()
                    window['song_name'].update(song_name)
                    window['song_status'].update('Playing:')

                except Exception as err:
                    pysg.popup_error(err)
