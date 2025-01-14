from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys

titles = []
descriptions = []
urls = []

# Writes the scraped data to a txt file and also writes the company name and link to application to another txt file.
def write_to_file():
	f = open('../data/formatted/application_links.txt', 'w', encoding='utf-8')
	j = open('../data/raw/scraped_text.txt', 'w', encoding='utf-8')

	for i in range(len(titles)):
		f.write(f'{titles[i]} -> {urls[i]}')
		f.write('\n')
		j.write(f'{descriptions[i]}')
		j.write('\n')

	f.close()
	j.close()

# Opens the provided url to the application posting and scrapes all descriptive text. 
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

# Crawls through each posting on the sidebar of the job postings page.
def crawl_sidebar(wd, url):
	wd.get(url)
	time.sleep(3)
	if "authwall" in wd.current_url:
		crawl_sidebar(wd, url)
		return

	html = wd.execute_script('return document.body.innerHTML')
	bs = BeautifulSoup(html, 'html.parser')

	sidebar = bs.find('ul', class_='jobs-search__results-list')

	i = 1

	listings = sidebar.find_all('li')
	for listing in listings:
		if not listing.div.a:
			continue
		url = listing.div.a['href']
		scrape_posting(wd, url)
		print(f'Scraping in progress...    {i}/{len(listings)}')
		i += 1
	
	print('Scraping Complete.')

def main():
	# This url can be modified for any type of query on LinkedIn.com/jobs via this variable, or be passed in via command line arguments
	# website_url = "https://www.linkedin.com/jobs/search?keywords=software%20engineering&location=&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"
	website_url = sys.argv[1]
	wd = webdriver.Chrome(executable_path='../Drivers/chromedriver.exe')

	crawl_sidebar(wd, website_url)
	write_to_file()
	wd.close()

if __name__ == "__main__":
	main()

