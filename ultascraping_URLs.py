from bs4 import BeautifulSoup
import requests
import re
import json

baseShampooURL = "https://www.ulta.com/shop/hair/shampoo-conditioner/shampoo"
baseConditionerURL = "https://www.ulta.com/shop/hair/shampoo-conditioner/conditioner"
baseOilURL = "https://www.ulta.com/shop/hair/treatment/oils-serums"
pageURL = "?page="

def scrapeProductPage():
	return

# review_counts = []

def scrapeProductsList(baseURL, pageN = 1):
	r = requests.get(baseURL + pageURL + str(pageN))
	print(r.status_code)

	productURLs = []

	# file = open('ulta_shampoos.csv', 'w', newline='')
	# writer = csv.writer(file)
	# csvheaders = ['Brand', 'Name', 'Review Content', 'Price', 'URL', 'ImgURL']
	# writer.writerow(csvheaders)


	# chrome_options = webdriver.ChromeOptions()
	# chrome_options.add_argument("--headless=new") #can remove =new for old headless (pre-109 chrome) mode
	# driver = webdriver.Chrome(options=chrome_options)
	# driver.get(URLname)


	# time.sleep(0.1) #wait for images to lazy load

	# html = driver.page_source
	html = r.content
	soupnames = BeautifulSoup(html, 'html5lib')

	namecol = soupnames.find('ul', attrs={'data-test':'products-list'})
	if namecol:
		productAs = namecol.find_all('a', attrs={'class':'pal-c-Link pal-c-Link--primary pal-c-Link--default'})
		for a in productAs:
			rating_div = a.find('div', attrs={'class':'ProductCard__rating'})
			if rating_div:
				num_reviews = rating_div.find('span', attrs={'class':'sr-only'})
				num_reviews = num_reviews.text
				num_reviews = re.search(r';\s*(\d+)\s*', num_reviews)
				num_reviews = int(num_reviews.group(1))
				# review_counts.append(num_reviews)
				if num_reviews >= 100:
					productURLs.append(a['href'])
	return productURLs

def scrapeUltaURLs():
	allShampooURLs = []
	allConditionerURLs = []
	allOilURLs = []
	# for i in range(1,2):
	# 	tempList = scrapeProductsList(baseShampooURL, pageN=i)
	# 	allShampooURLs += tempList
	for i in range(1,12):
		tempList = scrapeProductsList(baseShampooURL, pageN=i)
		allShampooURLs += tempList
	for i in range(1,12):
		tempList = scrapeProductsList(baseConditionerURL, pageN=i)
		allConditionerURLs += tempList
	for i in range(1,6):
		tempList = scrapeProductsList(baseOilURL, pageN=i)
		allOilURLs += tempList
	with open('shampoo_urls.json', 'w') as f:
		json.dump(allShampooURLs, f)
	with open('conditioner_urls.json', 'w') as f:
		json.dump(allConditionerURLs, f)
	with open('oil_urls.json', 'w') as f:
		json.dump(allOilURLs, f)
	
	# print("Total number of reviews, number of shampoo reviews, number of conditioner reviews, number of oil reviews: {}, {}, {}, {}".format(len(review_counts),len(allShampooURLs), len(allConditionerURLs), len(allOilURLs)))
	# poos_lt_100 = 0
	# conds_lt_100 = 0
	# oils_lt_100 = 0
	# for count in review_counts[:len(allShampooURLs)]:
	# 	if count < 100:
	# 		poos_lt_100 += 1
	# for count in review_counts[len(allShampooURLs):-len(allOilURLs)]:
	# 	if count < 100:
	# 		conds_lt_100 += 1
	# for count in review_counts[-len(allOilURLs):]:
	# 	if count < 100:
	# 		oils_lt_100 += 1
	# print("Number of shampoos, conditioners, oils with fewer than 100 reviews: {}, {}, {}".format(poos_lt_100, conds_lt_100, oils_lt_100))


	# allURLs = dict()
	# allURLs['Shampoo'] = allShampooURLs
	# allURLs['Conditioner'] = allConditionerURLs

	# with open('product_urls.json', 'w') as f:
	# 	json.dump(allURLs, f)
	


scrapeUltaURLs()
