import os
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("HTML/sample.html"), features = "html.parser")

for tag in soup.find_all(True):
    print(tag.name)
