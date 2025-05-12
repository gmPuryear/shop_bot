import requests 
from bs4 import BeautifulSoup
import json
import wm_bot

def main():
    print("hello from main!")
    wm_bot.get_wm_data()

if __name__ == "__main__":
    main()

