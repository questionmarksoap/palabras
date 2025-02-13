from bs4 import BeautifulSoup
import requests

page_to_scrape = requests.get(https://www.uscis.gov/newsroom/all-news?page=0)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
headlines = soup.findALL("span", attrs={"class":"field-content"})

for headline in headlines:
    print(headline.text)

