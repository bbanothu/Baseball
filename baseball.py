# # Import necessary packages
# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# import re
# # Site URL
# url="https://baseballsavant.mlb.com/daily_matchups"

# # Make a GET request to fetch the raw HTML content
# html_content = requests.get(url).text

# # Parse HTML code for the entire site
# soup = BeautifulSoup(html_content, "lxml")
# print(soup.prettify()) # print the parsed data of html

# # On site there are 3 tables with the class "wikitable"
# # The following line will generate a list of HTML content for each table
# gdp = soup.find_all("div", attrs={"class": "template__content template--one-column__content--one"})
# print("Number of tables on site: ",len(gdp))
# print(gdp) # print the parsed data of html

# # # Lets go ahead and scrape first table with HTML code gdp[0]
# # table1 = gdp[0]
# # # the head will form our column names
# # body = table1.find_all("tr")
# # # Head values (Column names) are the first items of the body list
# # head = body[0] # 0th item is the header row
# # body_rows = body[1:] # All other items becomes the rest of the rows

# # # Lets now iterate through the head HTML code and make list of clean headings

# # # Declare empty list to keep Columns names
# # headings = []
# # for item in head.find_all("th"): # loop through all th elements
# #     # convert the th elements to text and strip "\n"
# #     item = (item.text).rstrip("\n")
# #     # append the clean column name to headings
# #     headings.append(item)
# # print(headings)

# pluralsight.py
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # For linux/Mac
    # driver = webdriver.Chrome(options = chrome_options)
    # For windows
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe", options=chrome_options)
    return driver


def getTable(driver):
    # Step 1: Go to pluralsight.com, category section with selected search keyword
    driver.get(
        f"https://baseballsavant.mlb.com/daily_matchups")
    # wait for the element to load
    try:
        WebDriverWait(driver, 5).until(lambda s: s.find_element_by_id(
            "leaderboard").is_displayed())
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Step 3: Iterate over the search result and fetch the course
    course_page = soup.select("div.table-savant")
    return course_page


# create the driver object.
driver = configure_driver()
# run script
tableHtml = getTable(driver)
print(tableHtml)
# close the driver.
driver.close()
