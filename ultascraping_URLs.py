from bs4 import BeautifulSoup
import requests
# from selenium import webdriver
import json

baseShampooURL = "https://www.ulta.com/shop/hair/shampoo-conditioner/shampoo"
baseConditionerURL = "https://www.ulta.com/shop/hair/shampoo-conditioner/conditioner"
# baseOilURL = "https://www.ulta.com/shop/hair/treatment/oils-serums"
pageURL = "?page="

def scrapeProductPage():
	return

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
			if a.find('div', attrs={'class':'ProductCard__rating'}):
				productURLs.append(a['href'])
	return productURLs

def scrapeUltaURLs():
	allShampooURLs = []
	allConditionerURLs = []
	for i in range(1,12):
		tempList = scrapeProductsList(baseShampooURL, pageN=i)
		allShampooURLs += tempList
	for i in range(1,12):
		tempList = scrapeProductsList(baseConditionerURL, pageN=i)
		allConditionerURLs += tempList
	
	allURLs = dict()
	allURLs['Shampoo'] = allShampooURLs
	allURLs['Conditioner'] = allConditionerURLs

	with open('product_urls.json', 'w') as f:
		json.dump(allURLs, f)
	


scrapeUltaURLs()
