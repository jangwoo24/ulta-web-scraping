import requests
import time
import re
import json


baseDbUrl   = "https://display.powerreviews.com"
preUrl      = "/m/6406/l/en_US/product/"
postUrl     = "/reviews?paging.from=0&paging.size=25&sort=Oldest&image_only=false&page_locale=en_US"
postPostUrl = "&native_only=false&_noconfig=true&apikey=daa0f241-c242-4483-afb7-4449942d1a2b"
 

def scrapeReviewsSingleProduct(page_id):
    reviews_list = []
    # Input (Type 1):
    # https://www.ulta.com/p/product-name-pimprod######?sku=####
    # Turn into (Type 1):
    # https://display.powerreviews.com/m/6406/l/en_US/product/pimprod######
    # /reviews?paging.from=0&paging.size=25&sort=Oldest&image_only=false&page_locale=en_US
    # &native_only=false&_noconfig=true&apikey=daa0f241-c242-4483-afb7-4449942d1a2b
    reviews_dict = requests.get(url=baseDbUrl+preUrl+page_id+postUrl+postPostUrl).json()
    while 'paging' in reviews_dict and'next_page_url' in reviews_dict['paging']:
        print(baseDbUrl+reviews_dict['paging']['next_page_url']+postPostUrl)
        tempList = reviews_dict['results'][0]['reviews']
        reviews_list += tempList
        
        time.sleep(0.01)
        reviews_dict = requests.get(url=baseDbUrl+reviews_dict['paging']['next_page_url']+postPostUrl).json()
    #review parsing
    reviews_list = [
        {
        'product_id': x['details']['product_page_id'],
        'headline': x['details']['headline'], 
        'content':x['details']['comments'], 
        'helpfulness': x['metrics']['helpful_score']
        }
          for x in reviews_list]
    return reviews_list

  
def scrapeAllProductsFromFile(filename):
    all_reviews = []
    with open (filename, 'r') as f:
        urls_list = json.load(f)
    for productURL in urls_list:
        # page_id = re.search(r'(pimprod\d+|xlsImpprod\d+)', productURL).group(1)
        page_id = re.search(r'-([a-zA-Z]+\d+)', productURL).group(1)
        all_reviews += scrapeReviewsSingleProduct(page_id=page_id)
    return all_reviews


    

# read urls per product type (poo, cond, oil) from json files THEN scrape products and reviews
# url = "https://www.ulta.com/p/acidic-bonding-concentrate-shampoo-pimprod2022376?sku=2578815"
# scrapeReviewsSingleProduct(url)
all_poo_reviews = scrapeAllProductsFromFile('shampoo_urls.json')
with open('shampoo_reviews.json', 'w') as f:
    json.dump(all_poo_reviews, f)

all_cond_reviews = scrapeAllProductsFromFile('conditioner_urls.json')
with open('conditioner_reviews.json', 'w') as f:
    json.dump(all_cond_reviews, f)

all_oil_reviews = scrapeAllProductsFromFile('oil_urls.json')
with open('oil_reviews.json', 'w') as f:
    json.dump(all_oil_reviews, f)