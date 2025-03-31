import csv
from bs4 import BeautifulSoup
# import requests
from selenium import webdriver
import time


def scrapeUltaShampoos():
	# headers = {
 #        	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
 #    	}


	shampoos_info = []

	file = open('ulta_shampoos.csv', 'w', newline='')
	writer = csv.writer(file)
	csvheaders = ['Brand', 'Name', 'Rating', 'Price', 'URL', 'ImgURL']
	writer.writerow(csvheaders)

	URLname = "https://www.ulta.com/shop/hair/shampoo-conditioner/shampoo"
	#scrape url + "?page=N" N=1 to 10


	# headers = {
	#        	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
	#    	}
	# rnames = requests.get(URLname, headers=headers)
	# print(rnames)
	# soupnames = BeautifulSoup(rnames.content, 'html5lib')

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless=new") #can remove =new for old headless (pre-109 chrome) mode
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(URLname)


	# scrolling
 #
	# lastHeight = driver.execute_script("return document.body.scrollHeight")
	# pause = 0.1
	# while True:
	# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# 	time.sleep(pause)
	# 	newHeight = driver.execute_script("return document.body.scrollHeight")
	# 	if newHeight == lastHeight:
	# 		break
	# 	lastHeight = newHeight

	time.sleep(0.1) #

	html = driver.page_source
	soupnames = BeautifulSoup(html, 'html5lib')

	namecol = soupnames.find('ul', attrs={'data-test':'products-list'})
	# print(namecol)
	product_list_items = namecol.find_all('li', attrs={'data-test':'products-list-item'})
	for product_item in product_list_items:
		this_shampoo = {}
		product_card = product_item.find('div')
		product_link = product_card.find('a')
		image_card = product_link.find('div')
		content_card = product_link.find('div', attrs={'class':'ProductCard__content'})
		product_link = product_link.get("href")
		this_shampoo['url'] = product_link
		
		image_div = image_card.find('div')
		imageIMG = image_div.find('img')
		# print(imageIMG)
		imageURL = imageIMG.get("src")
		this_shampoo['imgURL'] = imageURL
		
		content_head = content_card.find('h3')
		brand_span = content_head.find('span')
		product_span = brand_span.find_next_sibling('span')
		brand_span = brand_span.find_next('span')
		product_span = product_span.find_next('span')
		brand_name = brand_span.text
		product_name = product_span.text
		this_shampoo['brand'] = brand_name
		this_shampoo['name'] = product_name
		
		rating_div = content_card.find('div').find_next('div')
		rating_span = rating_div.find('span')
		avg_rating_text = rating_span.text
		this_shampoo['avg_rating'] = avg_rating_text
		print(product_name)
		print(avg_rating_text)

		price_div = content_card.find('div').find_next_sibling('div')
		print(price_div)
		# price_div = price_div.find('div')

		price_span = price_div.find('span')
		price = price_span.text
		this_shampoo['price'] = price

		newheaders = ([brand_name, product_name, avg_rating_text, product_link, imageURL])
		writer.writerow(newheaders)
		shampoos_info.append(this_shampoo)
	return shampoos_info

scrapeUltaShampoos()
