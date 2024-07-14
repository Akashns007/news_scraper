from bs4 import BeautifulSoup as soup
import requests
from datetime import date
today = date.today()
d = today.strftime("%m-%d-%y")
print("date =", d)

cnn_url = "https://edition.cnn.com/world".format(d) #change this link biro


html = requests.get(cnn_url)

bsobj = soup(html.content,'lxml')


for link in bsobj.find_all("h2"):
    print("Headline : {}".format(link.text))

for news in bsobj.findAll('article',{'class':'headline__text inline-placeholder vossi-headline-primary-core-light'}):
    print(news.text.strip())


nbc_url = 'https://www.nbcnews.com/health/coronavirus'
r = requests.get('https://www.nbbcnews.com/health/coronavirus')
b = soup(r.content,'lxml')

for news in b.findAll('h2'):
    print(news.text.strip())

links=[]
for news in b.findAll('h2',{'class':'teaseCard_headline'}):
    links.append(news.a['href'])

for link in links:
    page = requests.get(link)
    bsobj = soup(page.content)
    for news in bsobj.findAll('div',{'class':'article-body_section article-body_last-section'}):
        print(news.text.strip())













































#last

