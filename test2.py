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
