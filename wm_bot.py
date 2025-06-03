import requests 
from bs4 import BeautifulSoup
import datetime as dt
import json

WM_URL = 'https://www.walmart.com/ip/24-PANINI-NFL-DONRUSS-OPTIC-VALUE-BOX/13580664574?classType=REGULAR&athbdg=L1600&from=/search'

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Accept-Languag': 'en-US,en;q=0.9',
}

def get_wm_product_data():
  # Get the web page
  res = requests.get(WM_URL, headers = headers)
  # Parse the web page
  parser = BeautifulSoup(res.text, 'lxml')
  # Locate the <script> tag containing the JSON data
  json_tag = parser.find("script", {"id": "__NEXT_DATA__"})
  # If the tag is found, parse the JSON data
  if json_tag:
    # parses the json string into readable format
    full_json_data =  json.loads(json_tag.string)
    # sliced_item_data = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]


    product_availability = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]["conditionOffers"][0]["availabilityStatus"]["value"]
    product_price = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]["conditionOffers"][0]["price"]["price"]

    print("product_availability: ", product_availability)
    print("product_price: ", product_price)
    
  
    # saves json data to file if json_tag is found
    with open("walmart_json_data.txt", "a", encoding = "utf-8") as file_to_write:
      current_date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      file_to_write.write("_______________________________ " + current_date_time + "_______________________________\n")
      # json.dump() writes the json data to file
      json.dump(full_json_data, file_to_write, indent = 4, ensure_ascii = False)

      print(f"<script> tag with id=__NEXT_DATA__ found and saved to 'walmart_json_data.txt' from {WM_URL}.")
  else:
    print(f"<script> tag with id=__NEXT_DATA__ not found on {WM_URL}.")

# def check_wm_product_availability():
#   if available, hit add to cart
#   Go to checkout
#   confirm item is in cart

