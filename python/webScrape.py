import os
import requests
from bs4 import BeautifulSoup

html_text = requests.get('https://www.boxofficemojo.com/weekly/?ref_=bo_nb_wey_secondarytab')
print(html_text)




'''
soup = BeautifulSoup(open("HTML/sample.html"), features = "html.parser")
for tag in soup.find_all(True):
    print(tag.name)
'''