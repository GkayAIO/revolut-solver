import base64, uuid, struct, random, requests, time, csv, json, datetime, os
from storage.colors import *

class Logger():

    def normal(message):
        print(fg.rs + f"[ Revolut ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.grey + " • " + fg.rs + f"{message}")

    def error(message):
        print(fg.rs + f"[ Revolut ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.grey + " • " + fg.red + f"{message}")

    def success(message):
        print(fg.rs + f"[ Revolut ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.grey + " • " + fg.green + f"{message}")

def clearConsole():
    try:
        os.system('cls')
    except:
        os.system('clear')
