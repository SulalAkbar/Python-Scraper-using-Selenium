from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup ,  NavigableString
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
#from selenium.webdriver.firefox.options import Options
import time
import csv
import random


options = webdriver.ChromeOptions()
options.add_argument("--headless") # Runs in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') # 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")



def info_scraper(soup):
	print('Got Soup')

	try:
		#product_title = soup.find('div',class_='row product-detail__info-container').find('h2',class_='is-blue').text
		dev = soup.find('h1',class_='is-blue')
		product_title = [element for element in dev if isinstance(element, NavigableString)]
		product_title = product_title.pop().strip()
	
	except Exception as e:
		print('product_title not')
		product_title = ''

	try:
		sachs = soup.find('div',class_='row product-detail__info-container').find('p',class_='is-lighter').text
	except Exception as e:
		print(' sachs Not ')
		sachs = ''

	try:	
		art_no = soup.find('span',class_='breadcrumbs__link').text
	except Exception as e:
		print(' art_no Not ')
		art_no = ''

	try:

		gtin = soup.find_all('h2',class_='not-margined-bottom like-a-paragraph')

		if len(gtin) > 2:
			gtin = gtin[0].text + '{}' + gtin[1].text
		else:
			gtin = gtin[0].text
	except Exception as e:
		print('GTIN Not ')
		gtin = ''

	try:	
		tarrif_no = soup.find_all('h2',class_='not-margined-bottom like-a-paragraph')
		
		if len(tarrif_no) > 2:
			tarrif_no = tarrif_no[2].text
		else:
			tarrif_no = tarrif_no[1].text

	except Exception as e:
		print(' tarrif Not ')
		tarrif_no = ''

	try:	
		application = soup.find_all('p',class_='not-margined-bottom')[6].text
	except Exception as e:
		print(' application Not ')
		application = ''

	try:	
		pack_unit = soup.find_all('p',class_='not-margined-bottom')[8].span.text
	except Exception as e:
		print(' pack_unit Not ')
		pack_unit = ''

	try:	
		pu_weight = soup.find('p',class_='not-margined-bottom shipping_condition').text
	except Exception as e:
		print('pu_weight Not ')
		pu_weight = ''
		
	try:
		#Product Details
		pt = soup.find('table',id='details-table__table--produktdetails')	
		#product_details = pt.text.strip().replace('\n\n\n\n\n','{}').replace('\n\n\n','{}').replace('\n','][')
		product_details = split(pt)
	except Exception as e:
		print('product_details Not ')
		product_details=''

	try:
		#Product Document Download
		dwnld_link = soup.find('table',class_='details-table__table--media').find('a').get('href')
	except Exception as e:
		print('dwnld_link Not ')
		dwnld_link=''

	#Application Compact Table

	try:
		compact_table = soup.find('table',id='details-table__table--kompakt')
		#compact_table = compact_table.text.strip().replace('\n',' : ')
		compact_table = compact_table.text.strip().replace('\n\n\n\n\n','{}').replace('\n\n\n','{}').replace('\n','][')
	except Exception as e:
		print('Not FOUND COMPACT TABLE')
		compact_table = ''

	#Application Detail
	try:
		detail_table = soup.find('table',class_='details-table__table--detailliert')
		#detail_table = detail_table.text.strip().replace('\n',' :')
		detail_table = detail_table.text.strip().replace('\n\n\n\n\n','{}').replace('\n\n\n','{}').replace('\n','][')
	except Exception as e:
		detail_table = ''

	#Image URL/ Calling Download Image Function
	try:
		img_url = soup.find('img',class_ = 'product-details__img')['src']
		print('Got Image URL ',img_url)
		img_downloader(img_url,art_no)
	except Exception as e:
		print('Error in Image (info scraper) :',e)





	print(product_title,'\n',sachs,'\n',art_no,'\n','GTIN :',gtin,'\n',tarrif_no,'\n',application,'\n',
		pack_unit,'\n',pu_weight,'\n','PRODUCT DETAILS',product_details,'\n','DOWNLOAD LINK',
		dwnld_link,'\n','COMPACT TABLE :',compact_table,'\n','DETAIL TABLE :',detail_table)

	data = {

		'product_title':product_title,
		'sachs' : sachs,
		'art_no': art_no,
		'gtin'  : gtin,
		'tarrif_no': tarrif_no,
		'application': application,
		'pack_unit': pack_unit,
		'pu_weight': pu_weight,
		'product_details_first':product_details['first'],
		'product_details_second':product_details['second'],
		'dwnld_link':dwnld_link,
		'compact_table': compact_table,
		'detail_table': detail_table

	}

	return data

#Function to split Product Details (Summary) Table in Two 

def split(pt):

	try:

		s = []
		o = []

		for i in pt.tbody.children:
			if i =='\n':
				pass
			else:
				t = []
				for j in i.children:
					if j == '\n':
						pass
					else:
						t.append(j.text)

				#print('------',t)
				o.append(t[:2])
				s.append(t[2:])

		#Reversing List
		# o = o.reverse()
		# s = s.reverse()
		first = ''
		for i in o:
			k =''
			for j in i:
				k = '  '+k +j +']['
			first = first + k + '{}'

		second = ''
		store = True
		for i in s:
			k =''
			for j in i:
				if j == '':
					store = False
				else:
					k = '  '+k +j +']['
			if store:
				second = second + k + '{}' 


		###########
		_list = []
		for i in pt.thead.tr.children:
			if i == '\n':
				pass
			else:
				_list.append(i.text)

		f = _list[:2]
		w = _list[2:]

		hf = ''
		for i in f:
			hf = hf + i +'][' 

		hl = ''
		for i in w:
			hl = hl + i + ']['

		first = hf + '{}' + first
		second = hl + '{}' + second

	except Exception as e:
		first = ''
		second = ''

	return {'first':first,'second':second}

#Function to read LINKS from CSV FIle
links = []
def link_reader():
	global links
	csv_file = open('links.csv')
	csv_reader = csv.reader(csv_file, delimiter=',')
	for r in csv_reader:
		links.append(r[0])

#Function to save data in CSV FILE
def csv_writer(info):
    file = "products.csv"
    csv_file = open(file, 'a', newline="\n",encoding="utf-8")
    writer = csv.writer(csv_file)
    writer.writerow([info['product_title'],info['sachs'],info['art_no'],info['gtin'],
    	info['tarrif_no'],info['application'],info['pack_unit'],info['pu_weight'],info['product_details_first'],
    	info['product_details_second'],info['dwnld_link'],info['compact_table'],info['detail_table']])
    csv_file.close()


def img_downloader(link,art_no):

	print('Downloading Image URL')
	
	retry = True
	while retry:
		r = requests.get(link)
		if r.status_code == 200:
			print('Got Image')
			retry = False
			with open('Images/'+art_no+'.jpg', 'wb') as f:
				f.write(r.content)
		else:
			time.sleep(random.randint(1,3))
			if r.status_code == 404:
				retry = False
			else:
				retry = True

header = {
	'product_title': 'PRODUCT TITLE',
	'sachs': 'SACHS',
	'art_no': 'ART NO.',
	'gtin': 'GTIN',
	'tarrif_no': 'TARRAIF NO.',
	'application': 'APPLICATION',
	'pack_unit': 'PACKAGING UNIT',
	'pu_weight': 'PU WEIGHT',
	'dwnld_link': 'DOWNLOAD LINK FILE',
	'product_details_first': 'PRODUCT DETAILS (Summary) FIRST',
	'product_details_second': 'PRODUCT DETAILS (Summary) SECOND',
	'compact_table': 'APPLICATION COMPACT (Suitable for)',
	'detail_table': 'APPLICATIONS DETAILED (Suitable for)',
}

website_URL = ''

brower = webdriver.Chrome(options=options,executable_path ="chromedriver.exe")
link_reader()
count = 0

csv_writer(header)
for i in links:
	try:
		brower.get(i)
		print('Got Page :', count+1)
		print('Browser Title :',brower.title)
	except Exception as e:
		print('Got Error In Getting Product Page : ',e)

	time.sleep(random.randint(4,6))
	soup = BeautifulSoup(brower.page_source, 'lxml')
	d = info_scraper(soup)
	csv_writer(d)
	count = count + 1


