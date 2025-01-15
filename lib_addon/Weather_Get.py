#//=============================================================================
# WinAra Assistent - Это ассистент для управления пк на базе Windows.
# Сделано FireSoft (By FireTIA)
#
# Сведения од модуле для WinAra Assistent:
#   1. Модуль предназначен для получения информации о погоде в вашем регионе
#   2. Модуль не содержит вредоносный скрипт.
#   3. Модуль не предназначен для поломки аппаратной и программной части.
#   4. Модуль использует API OpenWeather!
#
#   Особенность скрипта:
#   1. Файл конфигурации находится в папке lib_addon\Weather_Get\WRGet_Config.json
#   2. При изменении файла конфигурации не нужно будет перезапускать WinAra Assistent.
#
#       Автор модуля: FireTIA
#       Версия модуля: V0.1
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
import requests
from colorama import init, Fore, Back, Style
from datetime import datetime
from lib_addon import Play_Sound

init()


# ============== Settings

def load_config(file_path_dir_assistent):
    filename=f"{file_path_dir_assistent}\\lib_addon\\Weather_Get\\WRGet_Config.json"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", "Play", 0.3)
        print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Ошибка: файл '{filename}' не найден.")
        return None
    except json.JSONDecodeError:
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", "Play", 0.3)
        print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Ошибка: не удалось разобрать файл '{filename}'.")
        return None

def prepare_config(file_path_dir_assistent):
    global API_KEY, LAT, LON, UNITS, LANG, DEBUG_MODE, COUNTRY, TOWN, SYSTEM_WEATHER
    config = load_config(file_path_dir_assistent)

    if config:
        API_KEY = config.get("API_KEY")
        LAT = config.get("LAT")
        LON = config.get("LON")
        UNITS = config.get("UNITS")
        LANG = config.get("LANG")
        DEBUG_MODE = config.get("DEBUG_MODE")
        COUNTRY = config.get("COUNTRY")
        TOWN = config.get("TOWN")
        SYSTEM_WEATHER = config.get("SYSTEM_WEATHER")

        if DEBUG_MODE:
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Question.mp3", "Play", 0.6)
            print(f"\n\t\t\t\t\t{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} \n\n\t{Back.LIGHTWHITE_EX}{Fore.BLACK}ВНИМАНИЕ!! ПРИ ВКЛЮЧЕНОМ {Fore.BLUE}[DEBUG]{Fore.BLACK} РЕЖИМЕ ВЫ МОЖЕТЕ СПАЛИТЬ API КЛЮЧ OPENWEATHER !!{Back.RESET}{Fore.RESET} \n\t{Back.LIGHTWHITE_EX}{Fore.BLACK}ВНИМАНИЕ!! ПРИ ВКЛЮЧЕНОМ {Fore.BLUE}[DEBUG]{Fore.BLACK} РЕЖИМЕ ВЫ МОЖЕТЕ СПАЛИТЬ API КЛЮЧ OPENWEATHER !!{Back.RESET}{Fore.RESET} \n\t{Back.LIGHTWHITE_EX}{Fore.BLACK}ВНИМАНИЕ!! ПРИ ВКЛЮЧЕНОМ {Fore.BLUE}[DEBUG]{Fore.BLACK} РЕЖИМЕ ВЫ МОЖЕТЕ СПАЛИТЬ API КЛЮЧ OPENWEATHER !!{Back.RESET}{Fore.RESET}\n")
            select_entering = input(f"Enter - Продолжить | Отказаться от запуска модуля введите 'Cancel': {Fore.CYAN}")
            print(Fore.RESET)
            if select_entering.lower() in ["Cancel", "cancel", "c", "с", "отмена", "о", "Отмена"]:
                Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Exiting.mp3", "Play", 0.6)
                print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Отказ от запуска модуля.")
                return
            else:
                print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | {Fore.BLUE}[DEBUG]{Fore.RESET} API_KEY: {API_KEY}")
                print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | {Fore.BLUE}[DEBUG]{Fore.RESET} LAT: {LAT}, LON: {LON}")
                print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | {Fore.BLUE}[DEBUG]{Fore.RESET} UNITS: {UNITS}, LANG: {LANG}")
                print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | {Fore.BLUE}[DEBUG]{Fore.RESET} DEBUG_MODE: {DEBUG_MODE}")
                print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | {Fore.BLUE}[DEBUG]{Fore.RESET} COUNTRY: {COUNTRY}, TOWN: {TOWN}")
                print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | {Fore.BLUE}[DEBUG]{Fore.RESET} SYSTEM_WEATHER: {SYSTEM_WEATHER}")
                entering = " "

        
    else:
        print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Не удалось загрузить конфигурацию.")
        exit()

CoolDown = 0
# ============== Settings



def CoolDown_timer(in_v):
    global CoolDown
    CoolDown = in_v
    while CoolDown > 0:
        time.sleep(1)
        CoolDown -= 1

def parallel_task(in_v):
    CoolDown_timer(in_v)

def send_text(name_voice_assistant, text_analyse, file_path_dir_assistent):
    
    print(f"\n \n \t {Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | ВНИМАНИЕ У МОДУЛЯ ИМЕЮТСЯ НЕКОТОРЫЕ ПРОБЛЕМЫ! \n Рекомендуется воздержаться от использования")

    prepare_config(file_path_dir_assistent)

    weather_data = None

    print(f"\n{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Получение данных о погоде...")

    if CoolDown == 0:
        weather_data = get_weather_data(file_path_dir_assistent)
    else:
        print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Подождите пока пройдет CoolDown '{Fore.LIGHTBLUE_EX}{CoolDown}{Fore.RESET}'")
    

    if weather_data:
        print_weather_info(weather_data, file_path_dir_assistent)
    else:
        print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Ошибка получения данных о погоде.")


def get_weather_data(file_path_dir_assistent):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": UNITS,
        "lang": LANG,
    }

    try:
        response = requests.get(url, params=params)

        if DEBUG_MODE:
            print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | {Fore.BLUE}[DEBUG]{Fore.RESET} URL: {response.url}")
            print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | {Fore.BLUE}[DEBUG]{Fore.RESET} Response: {response.json()}")

        if response.status_code == 200:
            return response.json()
        else:
            Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", "Play", 0.3)
            print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Код ошибки: {response.status_code} \n\n\t\t{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} {Fore.LIGHTYELLOW_EX}| Если что включите в модуле дебаг {Fore.RESET} \n")
            return None
    except Exception as e:
        Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Error.wav", "Play", 0.3)
        print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Ошибка: {e} \n\n\t\t{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} {Fore.LIGHTYELLOW_EX}| Если что включите в модуле дебаг {Fore.RESET} \n")
        return None


def print_weather_info(data, file_path_dir_assistent):
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    wind_direction = get_wind_direction(data["wind"]["deg"])
    date_and_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    print(f"\n{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Погодная система: '{Fore.YELLOW}{SYSTEM_WEATHER}{Fore.RESET}'")
    print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Местоположение: '{COUNTRY}, {TOWN}'")
    print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Время: '{date_and_time}' \n")
    print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Температура: {temp}°C")
    print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Ощущается как: {feels_like}°C")
    print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Скорость ветра: {wind_speed} м/с, направление: {wind_direction}")
    print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Влажность: {humidity}%")
    print(f"{Fore.LIGHTYELLOW_EX}[Weather {Fore.LIGHTCYAN_EX}Addon]{Fore.RESET} | Давление: {pressure} гПа \n")

    Play_Sound.play_selector(f"{file_path_dir_assistent}\\Sound\\Notify_Complete.wav", "Play", 0.2)

    thread = threading.Thread(target=parallel_task(10))
    thread.start()
    thread.join()


def get_wind_direction(degree):
    directions = ["Северный", "Северо-восточный", "Восточный", "Юго-восточный", "Южный", "Юго-западный", "Западный", "Северо-западный"]
    index = round(degree / 45) % 8
    return directions[index]


