#//=============================================================================
# WinAra Assistent - Это ассистент для управления пк на базе Windows.
# Сделано FireSoft (By FireTIA)
#
# Сведения од модуле для WinAra Assistent:
#   1. Модуль предназначен для воиспроизведение звуков и аудио.
#   2. Модуль не содержит вредоносный скрипт.
#   3. Модуль не предназначен для поломки аппаратной и программной части.
#
#
#
#
#
#
#       Автор модуля: FireTIA
#       Версия модуля: V1
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

# === 
status_sound = "unmuted"
DEBUG = False
# ===

init()
if DEBUG:
    print(f"{Fore.LIGHTCYAN_EX}[Play Sound {Fore.BLUE}[DEBUG]{Fore.LIGHTCYAN_EX} ]{Fore.RESET} Start_Value | Состояние воиспроизведение звука: {Fore.LIGHTYELLOW_EX}status_sound = '{status_sound}'{Fore.RESET}")


def mute_sound(arg_in):
    global status_sound
    if arg_in == "muted":
        status_sound = "muted"
        
    elif arg_in == "unmuted":
        status_sound = "unmuted"

    if DEBUG:
        print(f"{Fore.LIGHTCYAN_EX}[Play Sound {Fore.BLUE}[DEBUG]{Fore.LIGHTCYAN_EX} ]{Fore.RESET} MS | Состояние воиспроизведение звука: {Fore.LIGHTYELLOW_EX}status_sound = '{status_sound}'{Fore.RESET}")


def play_sound(file_path, set_volume):
    if DEBUG:
        print(f"{Fore.LIGHTCYAN_EX}[Play Sound {Fore.BLUE}[DEBUG]{Fore.LIGHTCYAN_EX} ]{Fore.RESET} MSD | Состояние воиспроизведение звука: {Fore.LIGHTYELLOW_EX}status_sound = '{status_sound}'{Fore.RESET}")
    sound = pygame.mixer.Sound(file_path)
    if set_volume == None:
        sound.set_volume(0.6)
    else:
        sound.set_volume(set_volume)
    try:
        sound.play()
    except Exception as e:
        print(f"{Fore.LIGHTCYAN_EX}[Play Sound]{Fore.RESET} | Ошибка воспроизведения звука: {e}")



def play_selector(file_play, type_action, volume):
    if DEBUG:
        print(f"{Fore.LIGHTCYAN_EX}[Play Sound {Fore.BLUE}[DEBUG]{Fore.LIGHTCYAN_EX} ]{Fore.RESET} PS | Состояние воиспроизведение звука: {Fore.LIGHTYELLOW_EX}status_sound = '{status_sound}'{Fore.RESET}")
    if status_sound == "muted":
        return
    elif status_sound == "unmuted":
        if volume == None:
            volume = 0.6
        if type_action in ["play", "Play", "Played"]:
            play_sound(file_play, volume)
    else:
        print(f"{Fore.LIGHTCYAN_EX}[Play Sound]{Fore.RESET} | Не удалось определить состояние воиспроизведение звука: {Fore.LIGHTYELLOW_EX}status_sound = '{status_sound}'{Fore.RESET}")


