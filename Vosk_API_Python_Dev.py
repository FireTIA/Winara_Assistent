# / ==================================================
# GitHub: https://github.com/FireTIA/Winara_Assistent
# Автор: FireTIA
# \ ==================================================

import argparse
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os
import pygetwindow as gw
from colorama import init, Fore, Back, Style
import pygame
import time
import subprocess
from pynput.keyboard import Key, Controller
import keyboard
import re
from datetime import datetime
import logging
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
import random
import threading

# Стороние модули от FireSoft:
from lib_addon import Fun_Random_Word_exec
from lib_addon import Weather_Get
from lib_addon import Play_Sound
from lib_addon import LLM_Connect_oAI_JAN
#<<<



version_assistent = "0.3 BETA"


print(f"\n \n \n \t {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET} - Winara Assistent \n Версия: {Fore.LIGHTBLUE_EX}{version_assistent}{Fore.RESET} \n Links: {Fore.LIGHTBLUE_EX}https://github.com/FireTIA/Winara_Assistent{Fore.RESET} \n \n \n")


# Инициализация
script_directory = os.path.dirname(os.path.abspath(__file__))
init()
pygame.init()
pygame.mixer.init()
now = datetime.now()
formatted_time_date_startuped = now.strftime(f"%H-%M-%S=%Y-%m-%d")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Запуск распознавания речи с выбором модели.")
    parser.add_argument('--model', choices=['large', 'small'], default='small', help="Выбор модели: 'large' или 'small'. По умолчанию используется 'small'.")
    return parser.parse_args()

logging.basicConfig(
    filename=f"log\\log_assistent-{formatted_time_date_startuped}-.log",  # Имя файла для логирования
    level=logging.INFO,     # Уровень логирования (INFO, DEBUG, ERROR и т.д.)
    format="%(asctime)s - %(message)s",  # Формат записи
    datefmt="%H-%M-%S=%Y-%m-%d"  
)


# Чтение аргументов
args = parse_arguments()

# Путь к модели в зависимости от аргумента
if args.model == 'large':
    model_path = f"{script_directory}\\Module\\Speech_Recognition\\Vosk_API\\Models\\vosk-model-ru-0.42"
elif args.model == 'small':
    model_path = f"{script_directory}\\Module\\Speech_Recognition\\Vosk_API\\Models\\vosk-model-small-ru-0.22"


print(f"Используется модель: {model_path}")

# Загружаем модель
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Инициализация микрофона
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
stream.start_stream()



#---------------------
#-------------------------- Настройки
global internet_search_provider_url, loging, name_voice_assistant
name_voice_assistant = "Винара"
debug = "True" #True - Включен дебаг, False - Выключен дебаг
file_path_dir_assistent = f"{script_directory}"
internet_search_provider = "Yandex" # Yandex - Поиск через Яндекс, Google - Поиск через Google
loging = "True" #True - Включен логирование, False - Выключен логирование
command_file_path = "config\\commands.json"
word_volume_file_path = "config\\volume_in_word.json"
addon_Fun_Random_Word_exec = "False" #True - Включен модуль, False - Выключен модуль
addon_Weather_Get = "False" #True - Включен модуль, False - Выключен модуль
Use_Model_LLM_connect = "False" #True - Включен модуль, False - Выключен модуль
#-------------------------- Настройки
#---------------------

#------->>
#Аргументальные инструменты
global State_Sesion_Fun_Random_Word_exec
list_trued = ["True", "true", "on", "вкл", "Да", "ДА"]
list_false = ["False", "false", "off", "выкл", "Нет", "НЕТ", "None", "none"]

State_Sesion_Fun_Random_Word_exec = None
#
#<<-------



def log_event(event_message, type):
    if loging in ["True", "true"]:

        if type == "INFO":
            logging.info(event_message)
        elif type == "ERROR":
            logging.error(event_message)
        elif type == "WARNING":
            logging.warning(event_message)
        elif type == "CRITICAL":
            logging.critical(event_message)
        elif type == "DEBUG":
            logging.debug(event_message)
        else:
            logging.info(event_message)

if internet_search_provider == "Yandex":
    internet_search_provider_url = "https://www.yandex.ru/search?text="
    print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}I{Fore.GREEN}]{Fore.RESET} | Используется поисковая система: {Fore.LIGHTBLUE_EX}{internet_search_provider}{Fore.RESET}")
elif internet_search_provider == "Google":
    internet_search_provider_url = "https://www.google.com/search?q="
    print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}I{Fore.GREEN}]{Fore.RESET} | Используется поисковая система: {Fore.LIGHTBLUE_EX}{internet_search_provider}{Fore.RESET}")

if debug == "True":
    print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}D{Fore.GREEN}]{Fore.RESET} | Дебаг включен")
elif debug == "False":
    print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}D{Fore.GREEN}]{Fore.RESET} | Дебаг выключен")

if loging == "True":
    print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}D{Fore.GREEN}]{Fore.RESET} | Логирование включено {Fore.LIGHTBLUE_EX}'log_assistent-{formatted_time_date_startuped}.log'{Fore.RESET}")
elif loging == "False":
    print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}D{Fore.GREEN}]{Fore.RESET} | Логирование выключено")



log_event(f"Версия: {version_assistent}", "INFO")
log_event(f"Информация: час(ов) - минут(ы/а) - секунд(ы/a) = год-месяц-день", "INFO")
log_event(f"Используется модель: {model_path}", "INFO")
log_event(f"Текущие настройки: \n \t debug={debug} \n \t file_path_dir_assistent={file_path_dir_assistent} \n \t internet_search_provider={internet_search_provider} \n \t loging={loging} \n ===============================================", "INFO")
log_event(f"Говорите что-то", "INFO")
print("====|==============================================================")
print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}I{Fore.GREEN}]{Fore.RESET} | Запуск распознавания речи")
 
#--------------------------------------------------------




# Функция для закрытия активного окна
def close_active_window():
    try:
        # Получаем активное окно
        active_window = gw.getActiveWindow()
        if active_window is None:
            print("\n == Не удалось определить активное окно")
            log_event(f"Не удалось определить активное окно", "WARNING")
            return
        
        print(f"\n !=Закрытие окна: {Fore.LIGHTBLUE_EX}{active_window.title}{Fore.RESET}")
        log_event(f"Закрытие окна: {active_window.title}", "WARNING")
        active_window.close()  # Закрываем активное окно
    except Exception as e:
        log_event(f"Не удалось закрыть активное окно: {e}", "ERROR")
        print(f"\n == Не удалось закрыть активное окно: {e}")

def control_openrgb_led(action):
    # Подключение к серверу OpenRGB
    client = OpenRGBClient()

    # Список всех доступных устройств
    devices = client.devices

    if not devices:
        print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Устройство не обнаружено")
        log_event(f"[C] | Устройство управления подсветкой не обнаружено", "WARNING")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", f"play", 0.2 )
        
    else:
        device = devices[0]
        print(f"{Fore.LIGHTWHITE_EX}[o{Fore.LIGHTRED_EX}R{Fore.LIGHTGREEN_EX}G{Fore.LIGHTBLUE_EX}B{Fore.LIGHTWHITE_EX}] {Fore.RESET}| Управляю устройством: '{Fore.LIGHTYELLOW_EX}{device.name} | {device.type}{Fore.RESET}'")
        
        if action == "off_led":
            red_color = RGBColor(0, 0, 0)  
            device.set_color(red_color) 
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Выключил подсветку")
            log_event(f"[C] | Выключил подсветку", "INFO")

        elif action == "on_led":
            random_number = random.randint(1, 6)
            if random_number == 1:
                set_color = RGBColor(25, 25, 25)
                name_color = "Белый"
            if random_number == 2:
                set_color = RGBColor(25, 0, 0) 
                name_color = "Красный"
            if random_number == 3:
                set_color = RGBColor(0, 25, 0)  
                name_color = "Зеленый"
            if random_number == 4:
                set_color = RGBColor(0, 0, 25)
                name_color = "Синий"
            if random_number == 5:
                set_color = RGBColor(0, 21, 14)  
                name_color = "Берюзовый-ментоловый"
            if random_number == 6:
                set_color = RGBColor(27, 7, 0)
                name_color = "Тепло оранжевый"

            device.set_color(set_color) 
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Включил подсветку '{name_color}' ")
            log_event(f"[C] | Включил подсветку '{name_color}' / '{set_color}' ", "INFO")
        
        elif action == "set_color_blue":
            set_color = RGBColor(0, 0, 25)
            name_color = "Синий"
            device.set_color(set_color) 
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Установил цвет подсветки на '{Fore.LIGHTBLUE_EX}{name_color}{Fore.RESET}' ")
            log_event(f"[C] | Установил цвет подсветки на '{name_color}' / '{set_color}' ", "INFO")
        
        elif action == "set_color_red":
            set_color = RGBColor(25, 0, 0)
            name_color = "Красный"
            device.set_color(set_color) 
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Установил цвет подсветки на '{Fore.LIGHTRED_EX}{name_color}{Fore.RESET}' ")
            log_event(f"[C] | Установил цвет подсветки на '{name_color}' / '{set_color}' ", "INFO")
        
        elif action == "set_color_green":
            set_color = RGBColor(0, 25, 0)
            name_color = "Зеленый"
            device.set_color(set_color) 
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Установил цвет подсветки на '{Fore.LIGHTGREEN_EX}{name_color}{Fore.RESET}' ")
            log_event(f"[C] | Установил цвет подсветки на '{name_color}' / '{set_color}' ", "INFO")

        elif action == "set_color_white":
            set_color = RGBColor(25, 25, 25)
            name_color = "Белый"
            device.set_color(set_color) 
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Установил цвет подсветки на '{Fore.LIGHTWHITE_EX}{name_color}{Fore.RESET}' ")
            log_event(f"[C] | Установил цвет подсветки на '{name_color}' / '{set_color}' ", "INFO")

        elif action == "static_mode":
            modes = device.modes  # Получить доступные режимы
            for mode in modes:
                device.set_mode(modes[1])
            
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Включил статичную подсветку ")
            log_event(f"[C] | Включил статичную подсветку ", "INFO")
        
        elif action == "breathing_mode":
            modes = device.modes  # Получить доступные режимы
            for mode in modes:
                device.set_mode(modes[2])
            
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Включил режим дыхания подсветки ")
            log_event(f"[C] | Включил режим дыхания подсветки ", "INFO")

        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )


def paralel_task_weather_get(name_voice_assistant, text_analyse, file_path_dir_assistent):
    Weather_Get.send_text(name_voice_assistant, text_analyse, file_path_dir_assistent)

# Функция для выполнения команды
def execute_command(command_type, action, text_analyse):

    

    if command_type == "run_program":
        print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Запуск программы: {Fore.LIGHTCYAN_EX}{action}{Fore.RESET}")
        os.startfile(action)
        log_event(f"[C] | Запуск программы: {action}", "INFO")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )
    elif command_type == "exit_program":
        print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Выход из программы")
        log_event(f"[C] | Выход из программы", "INFO")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Exiting.mp3", f"play", 0.6 )
        time.sleep(1.5)
        exit()
    elif command_type == "close_window":
        print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Закрытие активного окна")
        close_active_window()
        log_event(f"[C] | Закрытие активного окна", "INFO")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )
    elif command_type == "open_url":
        print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Открытие сайта: {Fore.LIGHTCYAN_EX}{action}{Fore.RESET}")
        os.system(f"start {action}")
        log_event(f"[C] | Открытие сайта: {action}", "INFO")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2)
    elif command_type == "setting_assistent":
        global internet_search_provider_url
        global State_Sesion_Fun_Random_Word_exec
        if action == "off":
            Play_Sound.mute_sound("muted")
            print(f"{Fore.LIGHTGREEN_EX}[Cs]{Fore.RESET} | Выключил звук ассистента")
            log_event(f"[Cs] | Выключил звук ассистента", "INFO")
        elif action == "on":
            Play_Sound.mute_sound("unmuted")
            print(f"{Fore.LIGHTGREEN_EX}[Cs]{Fore.RESET} | Включил звук ассистента")
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2)
            log_event(f"[Cs] | Включил звук ассистента", "INFO")
        elif action == "set_search_provider_google":
            internet_search_provider_url = "https://www.google.com/search?q="
            print(f"{Fore.LIGHTGREEN_EX}[Cs]{Fore.RESET} | Установлен поисковик Google.com")
            log_event(f"[Cs] | Установлен поисковик Google.com", "INFO")
            
        elif action == "set_search_provider_yandex":
            internet_search_provider_url = "https://www.yandex.ru/search?text="
            print(f"{Fore.LIGHTGREEN_EX}[Cs]{Fore.RESET} | Установлен поисковик Yandex.ru")
            log_event(f"[Cs] | Установлен поисковик Yandex.ru", "INFO")


        elif action == "addon_Fun_RWexec_True":
            
            State_Sesion_Fun_Random_Word_exec = "True"
            print(f"{Fore.LIGHTGREEN_EX}[Caddon]{Fore.RESET} | Включен аддон '{Fore.LIGHTCYAN_EX}Fun_Random_Word_exec.py{Fore.RESET}' ")
            log_event(f"[Caddon] | Включен аддон 'Fun_Random_Word_exec.py' ", "INFO")
        
        elif action == "addon_Fun_RWexec_False":
            State_Sesion_Fun_Random_Word_exec = "False"
            print(f"{Fore.LIGHTGREEN_EX}[Caddon]{Fore.RESET} | Выключен аддон '{Fore.LIGHTCYAN_EX}Fun_Random_Word_exec.py{Fore.RESET}' ")
            log_event(f"[Caddon] | Выключен аддон 'Fun_Random_Word_exec.py' ", "INFO")
    elif command_type == "help_assistent":
        
        if action == "about_programm":
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | О программе")
            print(f"{Fore.LIGHTGREEN_EX}[AP]{Fore.RESET} | Голосовой ассистент {version_assistent}, предназначен для управления пк с помощью голоса. \n Версия: {version_assistent}")
            log_event(f"[C] | О программе", "INFO")
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2)

        if action == "about_command":
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | О командах")
            log_event(f"[C] | О командах", "INFO")
            print(f"{Fore.LIGHTGREEN_EX}[AP]{Fore.RESET} | Прочтите документацию к ПО/набору команд")
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2)

    elif command_type == "control_windows":
        
        if action == "minimize_window":
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Скрытие всех окон")
            gw.getAllWindows()
            for window in gw.getAllWindows():
                window.minimize()
                time.sleep(0.1)
            log_event(f"[C] | Скрытие всех окон", "INFO")
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2)
        
        if action == "maximize_window":
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Восстановление всех окон {Back.WHITE}{Fore.RED}(Не работает!){Back.RESET}{Fore.RESET}")
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", f"play", 0.2 )
            log_event(f"[C] | Восстановление всех окон (Не работает!)", "WARNING")
            return
            # Error Bug! Крашит проводник и саму Win, проверенно на Windows 10 22H2
            gw.getAllWindows()
            for window in gw.getAllWindows():
                window.maximize()
                time.sleep(0.1)
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )

        if action == "restart_explorer":
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Принудительная остановка {Fore.LIGHTBLUE_EX}'explorer.exe'{Fore.RESET} ")
            log_event(f"[C] | Принудительная остановка 'explorer.exe'", "INFO")
            subprocess.run('taskkill /f /im explorer.exe', shell=True)
            
            time.sleep(3)
            
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Запуск {Fore.LIGHTBLUE_EX}'explorer.exe'{Fore.RESET} ")
            log_event(f"[C] | Запуск 'explorer.exe'", "INFO")
            subprocess.run('start explorer.exe', shell=True)
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )

        if action == "block_windows":
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Блокировка рабочего стола")
            log_event(f"[C] | Блокировка рабочего стола", "INFO")
            ctypes.windll.user32.LockWorkStation()
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )

    

    elif command_type == "addon_weather":
        if action == "get_weather": 
            if addon_Weather_Get in list_trued:
                thread_weather_get = threading.Thread(
                    target=paralel_task_weather_get,
                    args=(name_voice_assistant, text_analyse, file_path_dir_assistent)
                    )
                thread_weather_get.start()
                

    elif command_type == "control_openrgb": 

        if action == "open_openrgb":
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Открытие программы {Fore.LIGHTBLUE_EX}'OpenRGB'{Fore.RESET}")
            log_event(f"[C] | Открытие программы 'OpenRGB'", "INFO")
            os.system(f'start {file_path_dir_assistent}\\Module\\OpenRGB_APP\\OpenRGB.exe')
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )
            print(f"{Fore.LIGHTYELLOW_EX}[Ch]{Fore.RESET} | 1. После запуска, перейдите во вкладку {Fore.LIGHTBLUE_EX}'Сервер SDK' {Fore.RESET}")
            print(f"{Fore.LIGHTYELLOW_EX}[Ch]{Fore.RESET} | 2. Ничего не изменяя, нажмите на кнопку {Fore.LIGHTBLUE_EX}'Запустить сервер' {Fore.RESET}")
            print(f"{Fore.LIGHTYELLOW_EX}[Ch]{Fore.RESET} | 3. Для управления подсветкой обратитесь к документации")

        if action == "openrgb_off_led":
            control_openrgb_led("off_led")
        
        if action == "openrgb_on_led":
            control_openrgb_led("on_led")

        if action == "openrgb_set_led_mode_static":
            control_openrgb_led("static_mode")
        
        if action == "openrgb_set_led_color_blue":
            control_openrgb_led("set_color_blue")
        
        if action == "openrgb_set_led_color_red":
            control_openrgb_led("set_color_red")
        
        if action == "openrgb_set_led_color_green":
            control_openrgb_led("set_color_green")
        
        if action == "openrgb_set_led_color_white":
            control_openrgb_led("set_color_white")

        if action == "openrgb_set_led_mode_breathing":
            control_openrgb_led("breathing_mode")


    else:
        print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | {Back.WHITE}{Fore.LIGHTRED_EX}Неизвестный тип команды{Back.RESET}{Fore.RESET}")
        log_event(f"[C] | Неизвестный тип команды", "WARNING")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", f"Play", 0.2 )

# Функция для исправления пробелов вокруг пунктуации
def fix_spacing(text):
    text = re.sub(r'\s+([,\.!?;:\)\]])', r'\1', text)
    text = re.sub(r'([,\.!?;:])(?=[^\s\)\]])', r'\1 ', text)
    return text






# Основная функция
def run_command(text_in, text_analyse):
    global commands  # Указываем, что будем обновлять глобальный объект `commands`
    
    text_in = text_in.lower().strip()  # Приведение текста к стандартному формату
    
    text_format = text_in.removeprefix(name_voice_assistant.lower()).strip()
    if debug == "True":
        print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}D{Fore.GREEN}]{Fore.RESET} | Текст после удаления слова '{name_voice_assistant.lower()}': {Fore.LIGHTBLUE_EX}{text_format}{Fore.RESET}")

    # Проверка на перезагрузку
    if text_format in ['перезапуск', 'перезагрузись', 'перезапустись']:
        commands, volume_words = load_commands(command_file_path, word_volume_file_path)
        print("Перезапуск конфигураций выполнен")
        log_event(f"[Cs] | Перезапуск конфигурации выполнен", "INFO")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Reload.mp3", f"play", 0.2 )
        return
    
    args_internet = ['поиск в интернете', 'поиск интернет', 'искать в интернете', 'найди в интернете']
    for args_internet in args_internet:
        if args_internet in text_format:
            if text_format.startswith(args_internet):
                text_format_search = text_format.removeprefix(args_internet.lower()).strip()
                print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Поиск в интернете: {Fore.LIGHTCYAN_EX}{text_format_search}{Fore.RESET}")
                log_event(f"[C] | Поиск в интернете: {text_format_search} \n \t URL: {internet_search_provider_url}{text_format_search} \n \n", "INFO")
                os.system(f'start {internet_search_provider_url}{text_format_search}')
                Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )
                return
            
    

    punctuation_map = {
        'символ запятая': ',',
        'символ точка': '.',
        'символ восклицательный знак': '!',
        'символ вопросительный знак': '?',
        'символ двоеточие': ':',
        'символ точка с запятой': ';',
        'символ кавычки': '"',
        'символ пробел': ' ',
        'символ скобка открывается': '(',
        'символ скобка закрывается': ')'
    }

    args_write_kb = ['напиши', 'напечатаю',' напечатай',  'напечатать', 'клавиатура']

    for args_write_kb in args_write_kb:
        if args_write_kb in text_format:
            if text_format.startswith(args_write_kb):
                # Удаляем префикс команды
                text_format_write_kb = text_format.removeprefix(args_write_kb.lower()).strip()

                # Заменяем голосовые команды на пунктуацию
                for word, symbol in punctuation_map.items():
                    text_format_write_kb = text_format_write_kb.replace(word, symbol)

                # Исправляем пробелы вокруг пунктуации
                text_format_write_kb = fix_spacing(text_format_write_kb)

                print(f"{Fore.LIGHTGREEN_EX}[Cw]{Fore.RESET} | Написал: {Fore.LIGHTCYAN_EX}{text_format_write_kb}{Fore.RESET}")
                keyboard.write(f'{text_format_write_kb}')
                log_event(f"[Cw] | Написал: {text_format_write_kb} ", "INFO")
                Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )
                return
    
    args_volume = ['измени громкость', 'поменяй громкость']
    for arg in args_volume:
        if arg in text_format:
            if text_format.startswith(arg):
                # Убираем префикс команды и обрабатываем текст
                text_format_search = text_format.removeprefix(arg.lower()).strip()
                
                # Преобразуем текст в уровень громкости
                volume_level = parse_volume_level(text_format_search)
                if volume_level is not None:
                    set_volume(volume_level)
                    Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", f"play", 0.2 )
                    return
                else:
                    print(f"{Fore.RED}[Ошибка]{Fore.RESET} Не удалось определить уровень громкости.")
                break

    # Перебираем все команды
    for command_type, command_list in commands.items():
        for command in command_list:
            if text_format in command["aliases"]:
                execute_command(command_type, command["action"], text_analyse)
                return
    
    print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | {Fore.LIGHTYELLOW_EX}Команда не найдена!{Fore.RESET}")
    log_event(f"[C] | Команда не найдена! \n \t V2Text{text_format} \n ", "WARNING")
    Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", f"play", 0.2 )



def load_commands(json_file_command, json_file_volume_in_word):
    try:
        # Загрузка команд 
        log_event(f"[System] | Открытие '{json_file_command}' ", "INFO")
        with open(json_file_command, "r", encoding="utf-8") as file:
            commands = json.load(file)

        # Загрузка словаря для громкости 
        log_event(f"[System] | Открытие '{json_file_volume_in_word}' ", "INFO")
        with open(json_file_volume_in_word, "r", encoding="utf-8") as file:
            volume_words = json.load(file)

        return commands, volume_words

    except FileNotFoundError as e:
        print(f"Файл не найден: {e.filename}")
        log_event(f"[System] | Файл не найден: {e.filename}", "ERROR")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", f"play", 0.2 )
        return {}, {}

    except json.JSONDecodeError as e:
        print(f"Ошибка чтения файла {e.filename}. Проверьте синтаксис JSON.")
        log_event(f"[System] | Ошибка чтения файла {e.filename}. Проверьте синтаксис JSON.", "ERROR")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", f"play", 0.2 )
        return {}, {}

# Загрузка данных из файлов
global commands, volume_words 
commands, volume_words = load_commands(command_file_path, word_volume_file_path)


def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        
        if 0 <= level <= 100:
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
            print(f"{Fore.LIGHTGREEN_EX}[C]{Fore.RESET} | Громкость изменена на: {level}%")
            log_event(f"[C] | Громкость изменена на: {level}%", "INFO")
        else:
            print(f"{Fore.RED}[Ошибка]{Fore.RESET} Уровень громкости должен быть от 0 до 100.")
            log_event(f"[Ошибка] | Уровень громкости должен быть от 0 до 100.", "INFO")
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", f"play", 0.2 )
    except Exception as e:
        print(f"{Fore.RED}[Ошибка]{Fore.RESET} Не удалось изменить громкость: {e}")
        log_event(f"[Ошибка] | Не удалось изменить громкость: {e}", "ERROR")
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", f"play", 0.2 )

def parse_volume_level(text):
    # Ищем одиночные числа
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    
    # Преобразуем текст в список слов
    words = text.lower().split()

    # Переменная для итогового значения
    total_value = 0
    for word in words:
        if word in volume_words:
            total_value += volume_words[word]

    # Если получилось найти уровень громкости, возвращаем его
    if total_value > 0:
        return total_value

    # Если не удалось определить уровень громкости
    return None


def handle_command(command, params):
    print(f"Обработка команды: {command} с параметрами: {params}")
    # Здесь можно вызвать функции основного кода, связанные с командой


try:
    log = 0
    while log < 1:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())


            text_analyse = result.get("text", "")
            if text_analyse == "":
                continue
            else:
                print(f"\n{Fore.LIGHTGREEN_EX}[SR]{Fore.RESET} | Распознанный текст: {Fore.LIGHTGREEN_EX}", result.get("text", ""), f"{Fore.RESET} \n")

            if addon_Fun_Random_Word_exec in list_trued:
                if State_Sesion_Fun_Random_Word_exec in list_trued:
                    Fun_Random_Word_exec.send_text(name_voice_assistant, text_analyse, file_path_dir_assistent)
            



            if text_analyse.startswith(name_voice_assistant.lower()):
                if debug in list_trued:
                    print(f"{Fore.GREEN}[{Fore.LIGHTBLUE_EX}D{Fore.GREEN}]{Fore.RESET} | Слово {Fore.LIGHTYELLOW_EX}'{name_voice_assistant.lower()}'{Fore.RESET} найдено в начале текста")
                    
                # Выполняем команду
                log_event(f"[DetectVoice2Text] | Слово '{name_voice_assistant.lower()}' найдено в начале текста. \n \t V2Text: {result.get("text", "")} ", "INFO")
                
                

                if Use_Model_LLM_connect in list_trued:
                    LLM_Connect_oAI_JAN.init_script(text_analyse, name_voice_assistant, handle_command)
                    
                elif Use_Model_LLM_connect in list_false:
                    run_command(result.get("text", ""), text_analyse)
                
            
except KeyboardInterrupt:
    Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Exiting.mp3", f"play", 0.6 )
    time.sleep(1.5)
    log_event(f"[Assistent] | Завершения работы программы", "INFO")
    print("\nПрограмма завершена.")
finally:
    stream.stop_stream()
    log_event(f"[System] | Остановка 'stream.stop_stream()' ", "INFO")
    stream.close()
    log_event(f"[System] | Закрытие 'stream.close()' ", "INFO")
    audio.terminate()
    log_event(f"[System] | Остановка 'stream.close()' ", "INFO")
