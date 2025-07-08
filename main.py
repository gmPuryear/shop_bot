import requests 
from bs4 import BeautifulSoup
import json
import wm_bot
import target_bot

def main():
    #Target bot
    target_bot.get_target_product_data()

if __name__ == "__main__":
    main()

