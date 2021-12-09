from selenium import webdriver
from bs4 import BeautifulSoup
import time

titles = []
descriptions = []
urls = []

def write_to_file():
	f = open('../data/raw/application_links.txt', 'w', encoding='utf-8')
	j = open('../data/raw/scraped_text.txt', 'w', encoding='utf-8')

	for i in range(len(titles)):
		f.write(f'{titles[i]} -> {urls[i]}')
		f.write('\n')
		j.write(f'{descriptions[i]}')
		j.write('\n')

	f.close()
	j.close()

def scrape_posting(wd, url):
	wd.get(url)
	time.sleep(5)

	if "authwall" in wd.current_url:
		scrape_posting(wd,url)
		return


	html = wd.execute_script('return document.body.innerHTML')
	bs = BeautifulSoup(html, 'html.parser')

	title = bs.find('a', class_='topcard__org-name-link topcard__flavor--black-link')
	description = bs.find('div', class_='description__text description__text--rich')
	titles.append(title.text.strip())
	descriptions.append(description.text.strip())
	urls.append(url)

def crawl_sidebar(wd):
	html = wd.execute_script('return document.body.innerHTML')
	bs = BeautifulSoup(html, 'html.parser')

	sidebar = bs.find('ul', class_='jobs-search__results-list')

	i = 1

	listings = sidebar.find_all('li')
	for listing in listings:
		url = listing.div.a['href']
		scrape_posting(wd, url)
		print(f'Scraping in progress...    {i}/{len(listings)}')
		i += 1
	
	print('Scraping Complete.')


website_url = "https://www.linkedin.com/jobs/search?keywords=software%20engineering&location=&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"
wd = webdriver.Chrome(executable_path='../Drivers/chromedriver.exe')
wd.get(website_url)

crawl_sidebar(wd)
write_to_file()
wd.close()



