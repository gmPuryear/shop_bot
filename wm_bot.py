import requests 
from bs4 import BeautifulSoup
import json

TARGET_URL  = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=93319179&is_bot=false&store_id=1922&pricing_store_id=1922&has_pricing_store_id=true&has_financing_options=true&include_obsolete=true&visitor_id=0196B52D689B0201A17612E28C03710C&skip_personalized=true&skip_variation_hierarchy=true&channel=WEB&page=%2Fp%2FA-93319179'
WM_URL = 'https://www.walmart.com/ip/24-PANINI-NFL-DONRUSS-OPTIC-VALUE-BOX/13580664574?classType=REGULAR&athbdg=L1600&from=/search'

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Accept-Languag': 'en-US,en;q=0.9',
}
# Get the web page
res = requests.post(TARGET_URL, headers = headers)
print(res.json())

# Parse the web page
parser = BeautifulSoup(res.text, 'html.parser')

# # Locate the <script> tag containing the JSON data
json_tag = parser.find("script", {"id": "__NEXT_DATA__"})
if json_tag:
#   # parses the json string into readable format
  full_json_data =  json.loads(json_tag.string)
# Prints the all data after converting python object to json string
  print(json.dumps(full_json_data, indent=4))

  sliced_item_data = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]
#   # sliced_item_data = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]["conditionOffers"][0]["availabilityStatus"]


  # saves json data to file if data is present
  with open("walmart_json_data.json", "w", encoding = "utf-8") as file_to_write:
    # json.dump() writes the json data to file
    json.dump(full_json_data, file_to_write, indent = 4, ensure_ascii = False)

    print("Full JSON data has been saved to 'walmart_json_data.json'.")

else:
  print("No JSON data not found on the page.")

