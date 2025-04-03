from bs4 import BeautifulSoup
import requests
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
import time
import re
import json


baseDbUrl   = "https://display.powerreviews.com"
preUrl      = "/m/6406/l/en_US/product/"
postUrl     = "/reviews?paging.from=0&paging.size=25&sort=Oldest&image_only=false&page_locale=en_US"
postPostUrl = "&native_only=false&_noconfig=true&apikey=daa0f241-c242-4483-afb7-4449942d1a2b"
 

def scrapeProductInfo(productURL):
    # scrape directly from productURL
    # Product Name, Brand Name, Price ($), Size (oz), Product Details?, INGREDIENTS
    return

def scrapeReviewsSingleProduct(productURL):
    reviews_list = []
    # Input (Type 1):
    # https://www.ulta.com/p/product-name-pimprod######?sku=####
    # Turn into (Type 1):
    # https://display.powerreviews.com/m/6406/l/en_US/product/pimprod######
    # /reviews?paging.from=0&paging.size=25&sort=Oldest&image_only=false&page_locale=en_US
    # &native_only=false&_noconfig=true&apikey=daa0f241-c242-4483-afb7-4449942d1a2b
    page_id = re.search(r'(pimprod\d+|xlsImpprod\d+)', productURL).group(1)
    reviews_dict = requests.get(url=baseDbUrl+preUrl+page_id+postUrl+postPostUrl).json()
    while 'next_page_url' in reviews_dict['paging']:
        print(baseDbUrl+reviews_dict['paging']['next_page_url']+postPostUrl)
        #do review scraping
        time.sleep(0.01)
        reviews_dict = requests.get(url=baseDbUrl+reviews_dict['paging']['next_page_url']+postPostUrl).json()

  


# read urls per product type (poo, cond, oil) from json files THEN scrape products and reviews
url = "https://www.ulta.com/p/acidic-bonding-concentrate-shampoo-pimprod2022376?sku=2578815"
scrapeReviewsSingleProduct(url)
