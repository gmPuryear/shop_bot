import requests
import json
import datetime as dt
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time

TARGET_BROWSER_URL = 'https://www.target.com/p/optic-4k-uhd-hdr-smart-tv-55in/-/A-93319179'
# URL to retrieve product info with get request
TARGET_GET_URL  = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=93319179&is_bot=false&store_id=1922&pricing_store_id=1922&has_pricing_store_id=true&has_financing_options=true&include_obsolete=true&visitor_id=0196B52D689B0201A17612E28C03710C&skip_personalized=true&skip_variation_hierarchy=true&channel=WEB&page=%2Fp%2FA-93319179'

params = {
    "key": "eb2551e4aa6e597b8c8e6fc4f2e1c7aa",  # Target's public API key for the PDP client
    "tcin": "93319179",                       # The TCIN for the Optic box
    "pricing_store_id": "3991",
    "has_pricing_store_id": "true"
}
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Accept-Languag': 'en-US,en;q=0.9',
}

def get_target_product_data():
  # Get the web page
  res = requests.get(TARGET_GET_URL, headers = headers, params = params)
  # Check if the request was successful
  if res.status_code == 200:
    # print all json data in the response
    full_product_data = res.json()

    product = full_product_data["data"]["product"]
    title = product["item"]["product_description"]["title"]
    price = product["price"]["formatted_current_price"]
    eligibility = product["item"]["eligibility_rules"]
    purchase_limit = product["item"]["fulfillment"]["purchase_limit"]
    # print(f"AAHHHH {purchase_limit}")
    print(f"{title} – {price} - Purchase limit: {purchase_limit} - Availability/eligibility goes here\n")

    check_in_stock()

    with open("target_json_data.txt", "a", encoding = "utf-8") as file_to_write:
      current_date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      file_to_write.write("\n_______________________________ " + current_date_time + "_______________________________\n")
      # json.dump() writes the json data to file
      json.dump(full_product_data, file_to_write, indent = 4, ensure_ascii = False)

      print(f"<script> tag with id=__NEXT_DATA__ found and saved to 'target_json_data.txt' from {TARGET_GET_URL}.")

  else:
    print(f"Error: {res.status_code} - not able to retrieve data from {TARGET_GET_URL}")

def check_in_stock():
  options = uc.ChromeOptions()
  options.headless = True  # Optional: run headless
  chrome_driver = uc.Chrome(options=options)

# Step 2: Go to Target product page
  chrome_driver.get(TARGET_BROWSER_URL)

  # Step 3: Wait for content to load
  time.sleep(3)

  # Step 4: Get the page source and parse it
  html = chrome_driver.page_source
  soup = BeautifulSoup(html, "html.parser")

  # Step 5: Check for 'Out of stock'
  out_of_stock_div = soup.find("div", {"data-test": "NonbuyableSection"})
  if out_of_stock_div:
      print("❌ Out of stock")
  else:
      print("✅ In stock or buyable")
  
    # parses the json string into readable format
    # full_json_data =  json.loads(res.string)
    # print(full_json_data)
    # sliced_item_data = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]


    # product_availability = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]["conditionOffers"][0]["availabilityStatus"]["value"]
    # product_price = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]["conditionOffers"][0]["price"]["price"]

    # print("product_availability: ", product_availability)
    # print("product_price: ", product_price)
    
  
    # saves json data to file if json_tag is found
  
  # else:
  #   print(f"<script> tag with id=__NEXT_DATA__ not found on {TARGET_URL}.")

# def check_wm_product_availability():
#   if available, hit add to cart
#   Go to checkout
#   confirm item is in cart