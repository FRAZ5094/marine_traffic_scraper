import dryscrape
import requests
from bs4 import BeautifulSoup

# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options

URL = "https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&current_port_in|begins|DUNDEE|current_port_in=735"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
}

session = dryscrape.Session()
session.visit(URL)
response = session.body()
soup = BeautifulSoup(response)

results = soup.find_all("section", class_="ag-grid-container ")

print(response)
