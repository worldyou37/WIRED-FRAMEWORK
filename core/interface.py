import os
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_type(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def glitch_msg(msg):
    print(f"\033[1;31m[!] {msg}\033[0m") # Texto em vermelho para destaque

def show_banner():
    banner = """
    \033[1;37m
    . . . . . . . . . . . . . . . . . . . . . . . . . 
    .  \033[1;30mCONNECTED TO THE WIRED\033[1;37m                      .
    .  \033[1;32mEverything is connected. Everything is data.\033[1;37m .
    . . . . . . . . . . . . . . . . . . . . . . . . . 
    \033[0m
    """
    print(banner)