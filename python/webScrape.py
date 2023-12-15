import os
import requests
from bs4 import BeautifulSoup

#get the website from requests

#html_text = requests.get('https://www.boxofficemojo.com/weekly/?ref_=bo_nb_wey_secondarytab')
#print(html_text)

#parse it with BeautifulSoup
soup = BeautifulSoup(open("HTML/weekly.html"), features = "html.parser")


#create a dictionary with this 

job = soup.find('table', class_ =
                "a-bordered a-horizontal-stripes a-size-base a-span12 mojo-body-table mojo-table-annotated scrolling-data-table")

print (job)














'''
soup = BeautifulSoup(open("HTML/sample.html"), features = "html.parser")
for tag in soup.find_all(True):
    print(tag.name)
'''