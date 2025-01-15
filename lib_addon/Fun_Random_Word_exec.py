#//=============================================================================
# WinAra Assistent - Это ассистент для управления пк на базе Windows.
# Сделано FireSoft (By FireTIA)
#
# Сведения од модуле для WinAra Assistent:
#   1. Модуль предназначен для приколов с пк пользователя, если он употребляет слова
#   2. Модуль не содержит вредоносный скрипт, скримеры.
#   3. Модуль не предназначен для поломки аппаратной и программной части.
#
#
#
#
#
#       Автор модуля: FireTIA
#       Версия модуля: V1.1
#\\=============================================================================

import os
import re
import random
import ctypes
from comtypes import CLSCTX_ALL
import time
import pyaudio
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pynput.keyboard import Key, Controller
import keyboard
import threading
import pygetwindow as gw
import json





def load_commands(file_path_dir_assistent_in):
    try:
        with open(f"{file_path_dir_assistent_in}\\lib_addon\\Fun_Random_Word_exec_Files\\bad_word.json", "r", encoding="utf-8") as file:
            bad_wordd = json.load(file)

        return bad_wordd

    except FileNotFoundError as e:
        print(f"Файл не найден: {e.filename}")
        play_sound(f"{file_path_dir_assistent_in}\\Sound\\Notify_Error.wav")
        return {}, {}

    except json.JSONDecodeError as e:
        print(f"Ошибка чтения файла {e.filename}. Проверьте синтаксис JSON.")
        play_sound(f"{file_path_dir_assistent_in}\\Sound\\Notify_Error.wav")
        return {}, {}

def send_text(name_voice_assistent, text_input, file_path_dir_assistent):
    global bad_words
    bad_words = load_commands(file_path_dir_assistent)
    check_text_in_VA(name_voice_assistent, text_input)
    action = check_words(text_input)
    active_execute_action(action, file_path_dir_assistent)

def check_text_in_VA(name_voice_assistent, text_input):
    if name_voice_assistent.lower() in text_input.lower():
        return

def check_words(text_input):
    found_bad_words = [word for word in bad_words if word in text_input]
    if found_bad_words:
        print(f"\n[Fun_RWexec] Обнаружены плохие слова: {', '.join(found_bad_words)}\n")

        # Выбираем случайное действие и выполняем его
        random_action = random.choice(actions)
        return random_action
    else:
       return None

def play_sound(file_path, set_volume):
    sound = pygame.mixer.Sound(file_path)
    if set_volume == None:
        sound.set_volume(0.8)
    else:
        sound.set_volume(set_volume)
    try:
        sound.play()
    except Exception as e:
        print(f"[Fun_RWexec]Ошибка воспроизведения звука: {e}")
    
def change_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)


def minimize_all_windows():
    gw.getAllWindows()
    for window in gw.getAllWindows():
        window.minimize()
        time.sleep(0.1)

def get_current_wallpaper():
    from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
    reg_path = r"Control Panel\Desktop"
    with OpenKey(HKEY_CURRENT_USER, reg_path) as key:
        return QueryValueEx(key, "WallPaper")[0]

actions = [1, 2, 3, 4, 5, 6, 7, 8]

def parallel_task(file_path_dir_assistent):
    play_sound(f"{file_path_dir_assistent}\\lib_addon\\Fun_Random_Word_exec_Files\\5-john-cena-theme-short.mp3", 0.3)

def active_execute_action(action, file_path_dir_assistent):
    if action is None:
        return

    if action == 1:
        os.system(f'start https://logos-pravo.ru/statya-561-koap-rf-oskorblenie')

    elif action == 2:
        os.system(f'start https://youtu.be/cKf3xsv_H60?t=16') 
    elif action == 3:
        os.system(f'start https://www.youtube.com/watch?v=FArpOP7ndNw') 
    elif action == 4:
        os.system(f'start https://www.youtube.com/watch?v=TW59mrlpbjg')
    elif action == 5:
        os.system(f'start https://wallhere.com/en/wallpaper/27422')
        time.sleep(8)
        ctypes.windll.user32.LockWorkStation()
        time.sleep(1)
        play_sound(f"{file_path_dir_assistent}\\lib_addon\\Fun_Random_Word_exec_Files\\4-crazy-realistic-knocking-sound-troll-twitch-streamers_small.mp3", 0.8)
    elif action == 6:

        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)

            volume.SetMasterVolumeLevelScalar(1 / 100.0, None)

        except Exception as e:
            play_sound(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav")
        
    elif action == 7:
        play_sound(f"{file_path_dir_assistent}\\lib_addon\\Fun_Random_Word_exec_Files\\1-vy-chio-vse-gei-choli-tut.mp3", 0.8)
        keyboard.press('w')
        time.sleep(6)
        keyboard.release('w')
        keyboard.press('d')
        time.sleep(3)
        keyboard.release('d')
    elif action == 8:
        thread = threading.Thread(target=parallel_task(file_path_dir_assistent))
        thread.start()
        thread.join()
        funny_wallpaper = f"{file_path_dir_assistent}\\lib_addon\\Fun_Random_Word_exec_Files\\funny_wallpaper_1.jpg"
        original_wallpaper = get_current_wallpaper()
        # Меняем обои
        change_wallpaper(funny_wallpaper)

        # Сворачиваем все окна
        minimize_all_windows()
        

        # Ждем некоторое время (10 секунд)
        time.sleep(60)

        # Восстанавливаем исходные обои
        change_wallpaper(original_wallpaper)

