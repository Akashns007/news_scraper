from bs4 import BeautifulSoup as soup
import requests
from datetime import date

# Get today's date
today = date.today()
d = today.strftime("%m-%d-%y")
print("Date =", d)

# # CNN URL
# cnn_url = "https://edition.cnn.com"
# html = requests.get(cnn_url)

# # Parse HTML content with BeautifulSoup
# bsobj = soup(html.content, 'lxml')

# # Find and print headlines
# print("CNN Headlines:")
# for link in bsobj.find_all("h3", class_="cd__headline"):
#     print("Headline:", link.text.strip())

# NBC URL
nbc_url = 'https://www.nbcnews.com/'
r = requests.get(nbc_url)
b = soup(r.content, 'lxml')

# Find and print headlines
print("\nNBC Headlines:")
for news in b.find_all('h2'):
    print(news.text.strip())

# Find and print article links and content
links = []
for news in b.find_all('h2', {'class': 'teaseCard__headline'}):
    if news.a:
        links.append(news.a['href'])

# Scrape each article link for its content
for link in links:
    if not link.startswith('http'):
        link = "https://www.nbcnews.com" + link  # Ensure the link is complete
    page = requests.get(link)
    bsobj = soup(page.content, 'lxml')
    for news in bsobj.find_all('div', {'class': 'article-body__section article-body__last-section'}):
        print(news.text.strip())
