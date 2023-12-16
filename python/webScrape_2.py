import os
import sys
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
from jinja2 import Environment, FileSystemLoader


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
        rank = row.find('td', class_ = "a-text-right mojo-header-column mojo-truncate mojo-field-type-rank mojo-sort-column")
        #type(rank) = str
        dic['rank'] = rank.string

        #LW Rank
        LW_rank = rank.next_sibling
        #type(LW_rank) = str
        dic['LW_rank'] = LW_rank.string

        #Movie
        movie = LW_rank.next_sibling
        dic['movie'] = movie.string

        #weeklyGross
        weeklyGross = movie.next_sibling
        dic['weeklyGross'] = weeklyGross.string

        #weeklyGrossChangeLW
        weeklyGrossChangeLW = weeklyGross.next_sibling
        dic['weeklyGrossChangeLW'] = weeklyGrossChangeLW.string

        #theaters
        theaters = weeklyGrossChangeLW.next_sibling
        dic['theaters'] = theaters.string

        #theatersChange
        theatersChange = theaters.next_sibling
        dic['theatersChange'] = theatersChange.string
        
        #perTheaterAVGGross
        perTheaterAVGGross = theatersChange.next_sibling
        dic['perTheaterAVGGross'] = perTheaterAVGGross.string
        
        #totalGross
        totalGross = perTheaterAVGGross.next_sibling
        dic['totalGross'] = totalGross.string

        #weeksReleased
        weeksReleased = totalGross.next_sibling
        dic['weeksReleased'] = weeksReleased.string

        #distributor
        distributor = weeksReleased.next_sibling
        if distributor.text == None:
            distributor = '-'
            dic['distributor'] = distributor
        else:
            dic['distributor'] = distributor.text.replace('\n', '')
        
        
        #append the dic to the list
        listOfDic.append(dic)
    
    for list in listOfDic:
        print(list)

    
    
    '''test write into html file'''
    with open('html/test.html', 'w') as html_file:
        for row in rows[1:31]:
            html_file.write(row.prettify())
            html_file.write('\n\n')

    return listOfDic



def send_email(sender, receivers, appPassword, html_file):
    #Write down the subject and the body of the email
    subject = 'Your Weekly Boxoffice Report'
    body = html_file
    
    #fill the em class with the content and other metadata
    for receiver in receivers:
        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)

        table = MIMEText(html_file, 'html')
        em.attach(table)
        
        #Use ssl to stay secure
        context = ssl.create_default_context()

        #Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
            smtp.login(sender, appPassword)
            smtp.sendmail(sender, receiver, em.as_string())



def weekly_html(listfOfDic):
    html_file = '''
    <html>
        <head></head>
        <body>
            <h2>Your Weekly Boxoffice Report</h2>
            <table>
                <tr>
                    <th>Rank</th>
                    <th>LW Rank</th>
                    <th>Movie</th>
                    <th>Weekly Gross</th>
                    <th>Weekly Gross Change LW</th>
                    <th>Theaters</th>
                    <th>TheatersChange</th>
                    <th>Per Theater AVG Gross</th>
                    <th>Total Gross</th>
                    <th>Weeks Released</th>
                    <th>Distributor</th>
                </tr>
                {% for obj in listOfDic %}
                    <tr>
                        <td>{{ listOfDic.rank }}</td>
                        <td>{{ listOfDic.LW_rant }}</td>
                        <td>{{ listOfDic.movie }}</td>
                        <td>{{ listOfDic.weeklyGross }}</td>
                        <td>{{ listOfDic.weeklyGrossChangeLW }}</td>
                        <td>{{ listOfDic.theaters }}</td>
                        <td>{{ listOfDic.theaterChange }}</td>
                        <td>{{ listOfDic.perTheaterAVGGross }}</td>
                        <td>{{ listOfDic.totalGross }}</td>
                        <td>{{ listOfDic.distributor }}</td>
                        <td>{{ listOfDic.weeksReleased }}</td>
                        
                    </tr>
            {% endfor %}
            </table>
        </body>
    </html>

'''
    
    
    return html_file

    


def main():
    weekly_listOfDic = mojo_weekly_scrape(weekly_website)
    html_file = weekly_html(weekly_listOfDic)
    send_email(sender, receiver, appPassword, html_file)

#Provide value for variables
weekly_website = "https://www.boxofficemojo.com/weekly/2023W49/?ref_=bo_wly_table_1"
sender = 'kytanmov@gmail.com'
receivers = ['ktan5@sva.edu', 'ddfzhh@foxmail.com']
appPassword = 'psjfdsycvcscpnvd'

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