import requests
import json
import os
import datetime as dt
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

load_dotenv()  # loads environment variables

TARGET_USERNAME = os.getenv('TARGET_USERNAME')
TARGET_PASSWORD = os.getenv('TARGET_PASSWORD')

# test target link for scraping
TARGET_BROWSER_URL = os.getenv('TARGET_BROWSER_URL')
TARGET_GET_URL  = os.getenv('TARGET_GET_URL')
TARGET_INSTOCK_STATUS_URL  = os.getenv('TARGET_INSTOCK_STATUS_URL')

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
    price = product_data["price"]["current_retail"]
    purchase_limit = product_data["item"]["fulfillment"]["purchase_limit"]
    print(f"{title} – {price} - Purchase limit: {purchase_limit} - Availability/eligibility goes here\n")
    with open("target_json_data.txt", "a", encoding = "utf-8") as file_to_write:
      current_date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      file_to_write.write("\n_______________________________ " + current_date_time + "_______________________________\n")
      # json.dump() writes the json data to file
      json.dump(full_product_data, file_to_write, indent = 4, ensure_ascii = False)
      print(f"<script> tag with id=__NEXT_DATA__ found and saved to 'target_json_data.txt' from {TARGET_GET_URL}.")
    # Check if the product is in stock
      check_in_stock(purchase_limit, price)
  else:
    print(f"Error: {res.status_code} - not able to retrieve data from {TARGET_GET_URL}")


def check_in_stock(purchase_limit, price):
  in_stock_res = requests.get(TARGET_INSTOCK_STATUS_URL, headers=headers)
  if in_stock_res.status_code == 200:
    in_stock_data = in_stock_res.json()
    shipping = in_stock_data["data"]["product"]["fulfillment"]["shipping_options"]
    print(price)
    if shipping["availability_status"] == "IN_STOCK" and shipping["available_to_promise_quantity"] > 0 and price < 35.00:
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
    # Check if the quantity dropdown exists
	# Click quantity drop down
    quantity_dropdown = chrome_driver.find_element(By.XPATH, quantity_dropdown_xpath)
    quantity_dropdown.click()
    chrome_driver.implicitly_wait(2)

    purchase_quantity = chrome_driver.find_element(By.CSS_SELECTOR, f'[aria-label="{purchase_limit}"]')
    purchase_quantity.click()

    wait = WebDriverWait(chrome_driver, timeout=10)
    add_to_cart_btn = chrome_driver.find_element(By.ID, "addToCartButtonOrTextIdFor94467903")
    wait.until(lambda _ : add_to_cart_btn.is_displayed())
    add_to_cart_btn.click()

    view_cart_and_checkout_btn = chrome_driver.find_element(By.LINK_TEXT, 'View cart & check out')
    wait.until(lambda _ : view_cart_and_checkout_btn.is_displayed())
    view_cart_and_checkout_btn.click()
    chrome_driver.implicitly_wait(2)

    sign_in_to_checkout_xpath = '/html/body/div[1]/div[2]/div[4]/div/div[2]/div/div/div[1]/div[3]/div/div/button'
    sign_in_to_checkout = chrome_driver.find_element(By.XPATH, sign_in_to_checkout_xpath).click()
    chrome_driver.implicitly_wait(2)

    login_username_field = chrome_driver.find_element(By.NAME, 'username')
    login_username_field.clear()  # Clear field
    login_username_field.send_keys(TARGET_USERNAME)  # Enter username text

    login_password_field = chrome_driver.find_element(By.NAME, 'password')
    login_password_field.clear()  # Clear field
    login_password_field.send_keys(TARGET_PASSWORD)  # Enter password text
    chrome_driver.implicitly_wait(2)

    signin_w_passwd_btn = chrome_driver.find_element(By.ID, 'login')
    signin_w_passwd_btn.click()
    chrome_driver.implicitly_wait(2)

# TODO: add a check if this button exists after a certain wait time, then if not, continue with the script this element may be not needed?
    skip_add_ph_num_btn = chrome_driver.find_element(By.LINK_TEXT, 'Skip')
    skip_add_ph_num_btn.click()
    chrome_driver.implicitly_wait(2)

    shipping_addy_radio_btn = chrome_driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/input')
    shipping_addy_radio_btn.click()

    checkout_save_and_continue_btn = chrome_driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[3]/div[4]/button')
    checkout_save_and_continue_btn.click()
    
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