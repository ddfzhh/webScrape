import os
import sys
import requests
from bs4 import BeautifulSoup

def mojo_weekly_scrape(weekly_website):
    #get the website from requests, and prepare the beautifulSoup object
    html_text = requests.get(weekly_website)
    soup = BeautifulSoup(html_text.content, 'html.parser')

    #initiate the dic
    dic = []

    #locate the area for the table, and put that into an variable
    moneys = soup.find_all('td', class_ = "a-text-right mojo-field-type-money")

    for money in moneys:
        print ('money = ')
        print(money.prettify())


def main():
    mojo_weekly_scrape(weekly_website)

#Provide value for variables
weekly_website = "https://www.boxofficemojo.com/weekly/2023W49/?ref_=bo_wly_table_1"

#run the function
main()
    










'''
1. Create a list of dictiondaries: [{'Rank' : 1, 'name':'The boy and the Heron', 'Gross':'$13,011,722'}
                                    {'Rank' : 2, 'name':'The Hunger Games', 'Gross':'$138,604,559'}]

2. Get the things into a email and send it to my email. Need to enable two steps verification. Need to have an app password. 
Also need to try to not hard code the password or email directly into the script. 

Use html to format the dictionaries in python, and generate an html table that will work in gmail. 
Think about design, metadata and scale. Make sure it is easily readable. 


'''