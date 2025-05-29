# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from wm_bot import WM_URL
# import time


# Checks your local Chrome version
# Finds the right ChromeDriver version
# Downloads and installs it automatically
# options = Options()
# # Headless mode = no UI is displayed
# # Regular mode = Chrome opens a real browser window you can see
# # options.add_argument("--headless")  # optional
# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()),
#     options=options
# )


# driver.get(WM_URL)

# time.sleep(10)
# driver.quit




import undetected_chromedriver as uc
from wm_bot import WM_URL
import time

driver = uc.Chrome()

driver.get(WM_URL)

# time.sleep(10)  # allows browser to be openn for 10 seconds then closes
# driver.quit()