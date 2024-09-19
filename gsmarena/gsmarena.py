import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SLEEP_DURATION = 2 # 1s causes throttling

def _main():

	with open('search_terms.txt') as file:
		model_short_names = [line.rstrip() for line in file]

	data = scrape_models(model_short_names)
	# for x in data:
	# 	print( x['model_name'], x['model_short_name'], x['ram'], x['release_year'], x['url'], sep="\t")

def scrape_models(model_short_names):
	driver = webdriver.Chrome()
	wait = WebDriverWait(driver, 4)
	data = []
	j = len(model_short_names)
	for i in range(j):
		model_short_name = model_short_names[i]
		model_url = search_model(driver, wait, model_short_name)

		model_name = None
		ram = None
		release_year = None

		if (model_url != None):
			model_name, ram, release_year = scrape_page(driver, wait, model_url)

		print(str(i) + '/' + str(j), model_name, model_short_name, ram, release_year, model_url, sep="\t")

		data.append({
			'model_name': model_name,
			'model_short_name': model_short_name,
			'ram': ram,
			'release_year': release_year,
			'url': model_url,
		})

	driver.close()
	return data

def search_model(driver, wait, model_short_name):
	url = "https://www.gsmarena.com/res.php3?sSearch=" + model_short_name
	driver.get(url)	
	try:
		element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#review-body > div > ul > li > a")))
		model_url = element.get_attribute('href')	
	except TimeoutException as ex:
		model_url = None
		

	driver.get('about:blank') # page change helps wait detection
	time.sleep(SLEEP_DURATION)

	return model_url

def scrape_page(driver, wait, url):
	driver.get(url)

	element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-spec='modelname']")))
	model_name = element.text
	element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-spec='internalmemory']")))
	ram = element.text
	element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-spec='year']")))
	release_year = element.text

	driver.get('about:blank') # page change helps wait detection
	time.sleep(SLEEP_DURATION)

	return model_name, ram, release_year


if __name__ == "__main__":
	_main()

