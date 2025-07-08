import requests 
from bs4 import BeautifulSoup
import json
import target_bot
import time

def main():
    while True:
        #target bot
        target_bot.get_target_product_data()
        time.sleep(10) # Delay for 5 seconds

if __name__ == "__main__":
    main()

