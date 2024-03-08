import requests
from bs4 import BeautifulSoup

url = "http://darklmmmfuonklpy6s3tmvk5mrcdi7iapaw6eka45esmoryiiuug6aid.onion.ly/images/images/"
response = requests.get(url).content
soup = BeautifulSoup(response, 'html.parser')
x = 0
for i in soup.findAll("a"):
    link = i.get("href")
    urls = "http:" + link
    op = open("pic"+str(x)+".jpg", "wb+")
    op.write(requests.get(urls).content)
    op.close()
    x += 1