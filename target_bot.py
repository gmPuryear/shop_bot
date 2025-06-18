import requests
import json
import datetime as dt
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Target Test Account Credentials
# Peter.frank.george@gmail.com
# 2felsman

# ACTUAL URL for scraping Target product data
# TARGET_BROWSER_URL = 'https://www.target.com/p/optic-4k-uhd-hdr-smart-tv-55in/-/A-93319179'
# ACTUAL URL to retrieve product info with standard get requests
# TARGET_GET_URL  = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=93319179&is_bot=false&store_id=1922&pricing_store_id=1922&has_pricing_store_id=true&has_financing_options=true&include_obsolete=true&visitor_id=0196B52D689B0201A17612E28C03710C&skip_personalized=true&skip_variation_hierarchy=true&channel=WEB&page=%2Fp%2FA-93319179'

# test target link for scraping
TARGET_BROWSER_URL = 'https://www.target.com/p/2024-panini-nfl-totally-certified-football-trading-card-blaster-box/-/A-94467903#lnk=sametab'
TARGET_GET_URL  = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=94467903&is_bot=false&store_id=1922&pricing_store_id=1922&has_pricing_store_id=true&has_financing_options=true&include_obsolete=true&visitor_id=0196B52D689B0201A17612E28C03710C&skip_personalized=true&skip_variation_hierarchy=true&channel=WEB&page=%2Fp%2FA-94467903'
TARGET_INSTOCK_STATUS_URL  = 'https://redsky.target.com/redsky_aggregations/v1/web/product_fulfillment_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&is_bot=false&tcin=94467903&store_id=1922&zip=76050&state=TX&latitude=32.340&longitude=-97.190&scheduled_delivery_store_id=1922&paid_membership=false&base_membership=false&card_membership=false&required_store_id=1922&visitor_id=0196B52D689B0201A17612E28C03710C&channel=WEB&page=%2Fp%2FA-94467903'

# Parameters for the Target API request
# Note: The API key and TCIN are specific to the product and should be updated accordingly.
params = {
    "key": "eb2551e4aa6e597b8c8e6fc4f2e1c7aa",  # Target's public API key for the PDP client
    # "tcin": "93319179",  # The TCIN for the ACTUAL Optic box
    "tcin": "94467903",     # The TCIN for the TEST Optic box               
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

    product_data = full_product_data["data"]["product"]
    title = product_data["item"]["product_description"]["title"]
    price = product_data["price"]["formatted_current_price"]
    purchase_limit = str(product_data["item"]["fulfillment"]["purchase_limit"])
    print(f"{title} – {price} - Purchase limit: {purchase_limit} - Availability/eligibility goes here\n")

    with open("target_json_data.txt", "a", encoding = "utf-8") as file_to_write:
      current_date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      file_to_write.write("\n_______________________________ " + current_date_time + "_______________________________\n")
      # json.dump() writes the json data to file
      json.dump(full_product_data, file_to_write, indent = 4, ensure_ascii = False)
      print(f"<script> tag with id=__NEXT_DATA__ found and saved to 'target_json_data.txt' from {TARGET_GET_URL}.")
    # Check if the product is in stock
      check_in_stock(purchase_limit)
  else:
    print(f"Error: {res.status_code} - not able to retrieve data from {TARGET_GET_URL}")


def check_in_stock(purchase_limit):
  in_stock_res = requests.get(TARGET_INSTOCK_STATUS_URL, headers=headers)
  if in_stock_res.status_code == 200:
    in_stock_data = in_stock_res.json()
    shipping = in_stock_data["data"]["product"]["fulfillment"]["shipping_options"]
    if shipping["availability_status"] == "IN_STOCK" and shipping["available_to_promise_quantity"] > 0:
      print("✅ Product is in stock!")
      add_product_to_cart(purchase_limit)
    else:
      print("❌ Product is out of stock.")
  else:
    print(f"Error: {in_stock_res.status_code} - not able to retrieve stock status from {TARGET_INSTOCK_STATUS_URL}")

def add_product_to_cart(purchase_limit):
  options = uc.ChromeOptions()
  options.headless = False  # Optional: run headless
  chrome_driver = uc.Chrome(options=options)
  try:
    chrome_driver.implicitly_wait(15)
    chrome_driver.get(TARGET_BROWSER_URL)
    
    print("Purchase limit: ", purchase_limit)

  # Get the html of the page
    html = chrome_driver.page_source
    quantity_dropdown_xpath = '//button[.//span[text()="Qty"]]'
	# Click quantity drop down
    quantity_dropdown = chrome_driver.find_element(By.XPATH, quantity_dropdown_xpath)
    quantity_dropdown.click()
    chrome_driver.implicitly_wait(2)

    purchase_quantity = chrome_driver.find_element(By.CSS_SELECTOR, f'[aria-label="{purchase_limit}"]')
    purchase_quantity.click()
    chrome_driver.implicitly_wait(2)

    add_to_cart = chrome_driver.find_element(By.ID, "addToCartButtonOrTextIdFor94467903").click()
    chrome_driver.implicitly_wait(2)

    view_cart_and_checkout = chrome_driver.find_element(By.LINK_TEXT, 'View cart & check out').click()
    chrome_driver.implicitly_wait(2)
    sign_in_to_checkout_xpath = '/html/body/div[1]/div[2]/div[4]/div/div[2]/div/div/div[1]/div[3]/div/div/button'
    sign_in_to_checkout = chrome_driver.find_element(By.XPATH, sign_in_to_checkout_xpath).click()

  except Exception as e:
        print("❌ item not added to cart: ", e)
  finally:
    time.sleep(999)
    chrome_driver.quit()


# ------chrome_driver.implicitly_wait(2) tells Selenium--------
# “If an element is not immediately found, keep polling for up to 2 seconds before throwing an exception.”
# That means:
# 	•	If the element is already available, execution continues immediately.
# 	•	If the element is not yet available, Selenium will retry for up to 2 seconds.
# It’s not a pause — it’s a grace period for finding elements.

# ****This checks for availability using web scraping*****
# def check_in_stock():
#   options = uc.ChromeOptions()
#   options.headless = True  # Optional: run headless
#   chrome_driver = uc.Chrome(options=options)

# # Step 2: Go to Target product page
#   chrome_driver.get(TARGET_BROWSER_URL)

#   # Step 3: Wait for content to load
#   time.sleep(3)

#   # Step 4: Get the page source and parse it
#   html = chrome_driver.page_source
#   soup = BeautifulSoup(html, "html.parser")

#   # Step 5: Check for 'Out of stock'
#   out_of_stock_div = soup.find("div", {"data-test": "NonbuyableSection"})
#   if out_of_stock_div:
#       print("❌ Out of stock")
#   else:
#       print("✅ In stock or buyable")



  
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