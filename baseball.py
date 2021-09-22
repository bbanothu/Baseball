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
from datetime import date
import os
import csv


def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # For Mac - Uncomment
    # driver = webdriver.Chrome(options=chrome_options)
    # For Windows - Uncomment
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
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find_all('table')
    tbody = table[-1].find_all('tbody')

    returnArrayRow = []
    tableHeaders = ["Batter", "Pitcher", "PA", "AB", "H", "2B", "3B", "HR", "SO", "K%",
                    "Whiff%", "BB", "BB%", "BA", "SLG", "wOBA", "xBA", "xSLG", "xwOBA", "EV", "LA"]
    returnArrayRow.append(tableHeaders)
    for tr in tbody[0].find_all('tr'):
        tds = tr.find_all('td')
        returnArrayCol = []
        for span in tds:
            current_val = span.find_all('span')
            if current_val:
                if current_val[0].text != '':
                    returnArrayCol.append(current_val[0].text)
        returnArrayRow.append(returnArrayCol)

    return returnArrayRow


def writeToCsv(data):
    # Get date for file name
    today = date.today()
    fileName = today.strftime("%m_%d_%Y")
    # Create file to store - has blank lines
    with open("init_file.csv", 'w', newline='') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(data)
    # Remove blank lines and write to actual file
    with open("init_file.csv", 'r') as inp, open(f"./output_files/{fileName}.csv", 'w') as out:
        for line in inp:
            if line.strip():
                out.write(line)
    # Delete Temp File
    os.remove("init_file.csv")


# create the driver object.
driver = configure_driver()
data = getTable(driver)
writeToCsv(data)
driver.close()
