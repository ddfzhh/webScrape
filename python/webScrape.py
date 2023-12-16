import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
from jinja2 import Environment, FileSystemLoader, Template
from helper import sender, receivers, appPassword


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

    return listOfDic



def send_email(sender, receivers, appPassword, html_template):
    #Write down the subject and the body of the email
    subject = 'Your Weekly Boxoffice Report'
    body = "This is your weekly movie report!"
    
    #fill the em class with the content and other metadata
    for receiver in receivers:
        em = MIMEMultipart()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        #em.set_content(body)

        table = MIMEText(html_template, 'html')
        em.attach(table)
        
        #Use ssl to stay secure
        context = ssl.create_default_context()

        #Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
            smtp.login(sender, appPassword)
            smtp.sendmail(sender, receiver, em.as_string())

        print(f'Successfully sent email to {receiver} from {sender}')



def weekly_html(listfOfDic):
    html = '''
    <html>
        <head>
        </head>
        <body>
            <h2 style="text-align:center;">Your Weekly Box Office Report (US)</h2>
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Rank</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">LW Rank</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Movie</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Weekly Gross</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Weekly Gross Change LW</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Theaters</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Theaters Change</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Per Theater AVG Gross</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Total Gross</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Weeks Released</th>
                    <th style="border:1px solid #dddddd; text-align:center; padding:8px;">Distributor</th>
                </tr>
                {% for obj in listOfDic %}
                    <tr>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.rank }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.LW_rank }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.movie }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.weeklyGross }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.weeklyGrossChangeLW }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.theaters }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.theatersChange }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.perTheaterAVGGross }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.totalGross }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.weeksReleased }}</td>
                        <td style="border:1px solid #dddddd; text-align:center; padding:8px;">{{ obj.distributor }}</td>
                        
                    </tr>
            {% endfor %}
            </table>
        </body>
    </html>

'''
    #Make the template and render the template:
    template = Template(html)
    html_template = template.render(listOfDic = listfOfDic)

    return html_template

    


def main():
    weekly_listOfDic = mojo_weekly_scrape(weekly_website)
    html_template = weekly_html(weekly_listOfDic)
    send_email(sender, receivers, appPassword, html_template)

#Provide value for variables
weekly_website = "https://www.boxofficemojo.com/weekly/2023W49/?ref_=bo_wly_table_1"
sender = 'kytanmov@gmail.com'
receivers = ['ktan5@sva.edu', 'kytan@foxmail.com']
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