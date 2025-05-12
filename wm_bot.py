import requests 
from bs4 import BeautifulSoup
import json

WM_URL = 'https://www.walmart.com/ip/24-PANINI-NFL-DONRUSS-OPTIC-VALUE-BOX/13580664574?classType=REGULAR&athbdg=L1600&from=/search'

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Accept-Languag': 'en-US,en;q=0.9',
}

def get_wm_data():
# Get the web page
  res = requests.post(WM_URL, headers = headers)
  # print(res.json())

  # Parse the web page
  parser = BeautifulSoup(res.text, 'html.parser')

  # # Locate the <script> tag containing the JSON data
  json_tag = parser.find("script", {"id": "__NEXT_DATA__"})
  if json_tag:
  #   # parses the json string into readable format
    full_json_data =  json.loads(json_tag.string)
  # Prints the all data after converting python object to json string
    print(json.dumps(full_json_data, indent=4))

    # sliced_item_data = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]
    sliced_item_data = full_json_data["props"]["pageProps"]["initialData"]["data"]["product"]["conditionOffers"][0]["availabilityStatus"]


    # saves json data to file if data is present
    with open("walmart_json_data.json", "w", encoding = "utf-8") as file_to_write:
      # json.dump() writes the json data to file
      json.dump(sliced_item_data, file_to_write, indent = 4, ensure_ascii = False)

      print("Full JSON data has been saved to 'walmart_json_data.json'.")

  else:
    print("No JSON data not found on the page.")

