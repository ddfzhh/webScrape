import os
import sys
import requests
from bs4 import BeautifulSoup

def mojo_weekly_scrape(weekly_website):
    #get the website from requests, and prepare the beautifulSoup object
    html_text = requests.get(weekly_website)
    soup = BeautifulSoup(html_text.content, 'html.parser')

    #initiate the list of listOfDic
    listOfDic = []
    n = 0

    #locate the area for the table
    table = soup.find('div', class_ = "a-section imdb-scroll-table-inner")

    #There are overall 36 '<tr' in the html. The first '<tr' is the header of the table. 
    #Therefore we can loop through the rest of the 35 "<tr" to get the data that we want. 
    rows = table.find_all('tr')
    for row in rows[1:31]:        #Skip the first iteration, which is the header, and I only need the top 30 movies in that week.
        
        #create a dic to store all the pairs to append to the list
        dic = {}
        #Rank
        rank = row.find('td', class_ = "a-text-right mojo-header-column mojo-truncate mojo-field-type-rank mojo-sort-column").text
        #type(rank) = str
        dic['rank'] = rank

        #LW Rank
        LW_rank = row.find('td', class_="a-text-right mojo-field-type-positive_integer").text
        #type(LW_rank) = str
        dic['LW_rank'] = LW_rank

        #Movie
        movie = row.find('a', class_ = "a-link-normal").text
        dic['movie'] = movie

        #weeklyGross
        weeklyGross = row.find('td', class_="a-text-right mojo-field-type-money mojo-estimatable").text
        dic['weeklyGross'] = weeklyGross

        #weeklyGross_soup
        weeklyGross_soup = row.find('td', class_ ="a-text-right mojo-field-type-money mojo-estimatable")
        grossChangeWeekly = weeklyGross_soup.next_sibling.string #get it based on the previous element since there are different pattern for this part
        dic['grossChangeWeekly'] = grossChangeWeekly
        
        #append the dic to the list
        listOfDic.append(dic)
    for list in listOfDic:
        print(list)
    '''
    
    '''





    '''test write into html file'''
    with open('html/test.html', 'w') as html_file:
        for row in rows[1:31]:
            html_file.write(row.prettify())
            html_file.write('\n\n')
    

    


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