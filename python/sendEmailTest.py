import os
import sys
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import ssl
import smtplib


def send_email(sender, receiver, appPassword):
    #Write down the subject and the body of the email
    subject = 'Your Weekly Boxoffice Report'
    body = "How old are you? "
    
    #fill the em class with the content and other metadata
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)
    
    #Use ssl to stay secure
    context = ssl.create_default_context()

    #Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
        smtp.login(sender, appPassword)
        smtp.sendmail(sender, receiver, em.as_string())


def main():
    send_email(sender, receiver, appPassword)


#Provide value for variables
weekly_website = "https://www.boxofficemojo.com/weekly/2023W49/?ref_=bo_wly_table_1"
sender = 'kytanmov@gmail.com'
receiver = 'ktan5@sva.edu'
appPassword = 'psjfdsycvcscpnvd'

#run the function
main()