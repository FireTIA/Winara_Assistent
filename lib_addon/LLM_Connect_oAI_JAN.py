#//=============================================================================
# WinAra Assistent - Это ассистент для управления пк на базе Windows.
# Все что связанно с WinAra Assistent не подлежит продаже и распространению! 
# Сделано FireSoft (By FireTIA)
#
# Сведения од модуле для WinAra Assistent:
#   1. Модуль полностью изменяет функционал и поведение WinAra Assistent
#   2. Модуль не содержит вредоносный скрипт.
#   3. Модуль может повредить ваш пк на программном уровне!
#   4. У модуля высокие требования к аппаратной части железа. (CPU + RAM or GPU + VRAM) При использовании JAN.AI!
#   5. Изменения модуля строго запрещен, и его передача для других лиц. Без проверки FireSoft на код.
#
#
#
#
#
#       Автор модуля: FireTIA
#       Версия модуля: V0.1 BETA!!!!
#\\=============================================================================


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

import openai
from colorama import Fore, Style, init
# Инициализация colorama
init(autoreset=True)

# Укажите локальный API
openai.api_base = "http://127.0.0.1:1337/v1"  # Локальный API для JAN.AI
openai.api_key = "no-key-jan"  # API-ключ для OpenAI

# Инициализация контекста
messages = [{"role": "system", "content": "Вы - WinAra, виртуальный персонаж. Вы можете общаться и выполнять команды с триггерами по запросу пользователя. Если пользователь просит выполнить команду, вы пишете точный триггер. Пример: '-led-on' включает подсветку."}]



def command_t_execute_on_pc(in_triger_command):
    
    if in_triger_command in ["-led-on", "-leds-on"]:
        print(Fore.CYAN + "Выполняю: включаю подсветку.")
    elif in_triger_command in ["-led-off", "-leds-off"]:
        print(Fore.CYAN + "Выполняю: выключаю подсветку.")
    elif in_triger_command in ["-start-browser", "-start-browsers"]:
        print(Fore.CYAN + "Выполняю: Запускаю браузер.")




def trim_context():
    """Ограничивает длину контекста сообщений."""
    global messages
    total_length = sum(len(msg['content']) for msg in messages)
    while total_length > 1500:  # Лимит длины контекста
        messages.pop(1)  # Удаляем старейшее сообщение (первое после system)
        total_length = sum(len(msg['content']) for msg in messages)


def clear_context():
    """Сбрасывает контекст сообщений."""
    global messages
    messages = [{"role": "system", "content": "Вы - WinAra, виртуальный персонаж. Вы можете общаться и выполнять команды с триггерами по запросу пользователя. Если пользователь просит выполнить команду, вы пишете точный триггер. Пример: '-led-on' включает подсветку."}]
    print(Fore.YELLOW + "Контекст сообщений очищен.")


def print_message(role, message, animate=False):
    """Выводит сообщения с опцией анимации текста."""
    if role == "user":
        print(Fore.GREEN + Style.BRIGHT + f"Вы: {message}")
    elif role == "assistant":
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"WinAra: {message}")
    else:
        print(Fore.YELLOW + Style.BRIGHT + f"{role}: {message}")


# Список доступных триггеров команд
command_triggers = {
    "-led-on": lambda: command_t_execute_on_pc("-led-on"),
    "-led-off": lambda: command_t_execute_on_pc("-led-off"),
    "-start-browser": lambda: command_t_execute_on_pc("-start-browser"),
}


def execute_triggered_command(reply):
    """Выполняет команду на основе триггера в ответе LLM."""
    for trigger, action in command_triggers.items():
        if trigger in reply:
            action()  # Выполняем действие
            return True
    return False


def is_command_request(text):
    """Определяет, является ли текст запросом команды."""
    command_keywords = ["включи", "выключи", "подсветка", "команда"]
    return any(keyword in text for keyword in command_keywords)


def connect_LLM(in_cl_Text):
    """Отправляет запрос в LLM и обрабатывает ответ."""
    global messages
    messages.append({"role": "user", "content": in_cl_Text})
    trim_context()  # Ограничиваем длину контекста

    try:
        # Выбираем контекст в зависимости от запроса
        is_command = is_command_request(in_cl_Text)
        if is_command:
            messages[0]["content"] = (
                "Вы - WinAra, виртуальный персонаж. Пользователь просит выполнить команду. "
                "Вы должны ответить кратко и точно, добавив соответствующий триггер, например: '-led-on'."
                "Все триггеры: '-led-on', '-led-off', '-start-browser' "
            )
        else:
            messages[0]["content"] = (
                "Вы - WinAra, виртуальный персонаж. Вы можете общаться, отвечать на вопросы и поддерживать разговор."
            )

        # Генерация ответа
        response = openai.ChatCompletion.create(
            model="llama3.1-8b-instruct",
            messages=messages,
            max_tokens=200,
            temperature=0.8,
            top_p=0.9,
        )
        assistant_reply = response.choices[0].message['content']

        print_message("Вы", in_cl_Text)
        print_message("assistant", assistant_reply, animate=True)

        messages.append({"role": "assistant", "content": assistant_reply})

        # Проверяем триггеры команд
        if is_command:
            if not execute_triggered_command(assistant_reply):
                print(Fore.YELLOW + "Нет триггеров для выполнения команд.")

    except Exception as e:
        print(Fore.RED + f"Произошла ошибка: {e}")


def init_script(in_SR_Text, name_vc_assistant, callback):
    """Инициализирует взаимодействие с пользователем."""
    in_SR_Text_f1 = in_SR_Text.lower().strip()
    in_SR_Text_f2 = in_SR_Text_f1.removeprefix(name_vc_assistant.lower()).strip()

    print(Fore.YELLOW + "Добро пожаловать в чат с Винарой! Скажите 'выход', чтобы завершить.\n")
    if in_SR_Text_f2 == "забудь контекст":
        clear_context()
    else:
        connect_LLM(in_SR_Text_f2)