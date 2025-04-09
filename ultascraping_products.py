from bs4 import BeautifulSoup
import requests
import time
import re
import json

IMG_SIZE = 200
BASE_IMG_URL = "https://media.ulta.com/i/ulta/"
POST_IMG_URL = "?w={}&h={}&fmt=auto".format(IMG_SIZE, IMG_SIZE)

def scrapeSingleProductInfo(productURL):
    r = requests.get(productURL)
    print(r.status_code)
    html = r.content
    
    soup = BeautifulSoup(html, 'html5lib')
    #soup.find(...) etc
    productInfoDiv = soup.find('div', attrs={'class':'ProductInformation'})
    brand_name = productInfoDiv.find('a').text
    product_name = productInfoDiv.find('span', attrs={'class':'Text-ds Text-ds--title-5 Text-ds--left Text-ds--black'}).text
    
    avg_stars = soup.find('div', attrs={'class':'ReviewStars__Content'})
    avg_stars = avg_stars.find('span').text

    product_price = soup.find('div', attrs={'class':'ProductPricing'})
    #If sales price exists, get original price, else just get price
    if product_price.find('span', class_='Text-ds Text-ds--title-5 Text-ds--left Text-ds--black'):
        product_price = product_price.find('span').text
    else:
        product_price = product_price.find('span', class_='Text-ds Text-ds--body-3 Text-ds--left Text-ds--neutral-600 Text-ds--line-through').text
    product_price = float(product_price.replace('$',''))

    # product_size = soup.find_all('div', attrs={'class':'ProductDimension'})[-1]
    # product_size = product_size.find('span', attrs={'class':'Text-ds Text-ds--body-3 Text-ds--left Text-ds--black'}).text
    # product_size = float(re.search(r'(\d+(?:.\d+)?) oz', product_size).group(1))
    # no longer including size

    summaryCard = soup.find('div', attrs={'class':'SummaryCard'})
    ethical_values = []
    if summaryCard: #then add the "Conscious Beauty" values to the list
        summaryCard = summaryCard.find_all('span', attrs={'class':'Text-ds Text-ds--body-2 Text-ds--left Text-ds--black'})
        for valuesSpan in summaryCard:
            ethical_values.append(valuesSpan.text)
    
    ingredients_list = soup.find_all('div', attrs={'class':'pal-c-Accordion__body--inner'})[-1]
    ingredients_list = ingredients_list.find('p').text
    ingredients_list = ingredients_list.split(', ')

    
    sku = re.search(r'sku=(\d+)', productURL).group(1)
    img_url = BASE_IMG_URL + sku + POST_IMG_URL



    
    # JSON should use page_id as key, list of features as value
    # Product Name, Brand Name, Avg Rating (1-5), Price ($), Size (oz), Product Details?, INGREDIENTS (list?), productURL, imgURL?
    return {
        'product'       :   product_name,
        'brand'         :   brand_name,
        'rating'        :   avg_stars, #float
        'price'         :   product_price, #float
        # 'size'          :   product_size, #float, ounces
        'values'        :   ethical_values, #list, could be empty
        'ingredients'   :   ingredients_list,
        'url'           :   productURL,
        'imgUrl'        :   img_url
            }


def scrapeAllProductsFromFile(filename):
    # save into dict with page_id as keys,
    # dict output of scrapeSingleProductInfo()
    #   as values
    # this dict should ultimately be saved 
    #   as value of ANOTHER with product type 
    #   as keys (i.e, "shampoo": ...)
    all_productInfo = dict()
    with open(filename, 'r') as f:
        urls_list = json.load(f)
    for productURL in urls_list:
        print(productURL)
        page_id = re.search(r'-([a-zA-Z]+\d+)', productURL).group(1)
        all_productInfo[page_id] = scrapeSingleProductInfo(productURL)
        time.sleep(0.1)

    return all_productInfo


with open('products.json', 'w') as f:
    all_poo_products = scrapeAllProductsFromFile('shampoo_urls.json')
    print(all_poo_products)
    all_cond_products = scrapeAllProductsFromFile('conditioner_urls.json')
    print(all_cond_products)
    all_oil_products = scrapeAllProductsFromFile('oil_urls.json')
    print(all_oil_products)
    all_products = {
        'shampoo'       :   all_poo_products,
        'conditioner'   :   all_cond_products,
        'oil'           :   all_oil_products
    }
    print(all_poo_products)
    json.dump(all_products, f)


# url = "https://www.ulta.com/p/everpure-sulfate-free-glossing-conditioner-lasting-shine-pimprod2049541?sku=2633795"
# url = "https://www.ulta.com/p/acidic-bonding-concentrate-shampoo-pimprod2022376?sku=2578815&pr_rd_page=1#reviews"
# print(scrapeSingleProductInfo(url))