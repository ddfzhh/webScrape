# Weekly Box Office Email
#### Video Demo:  (https://youtu.be/Fe-n8KmPfII)

### Description
This is my final project for CS50's Intro to Computer Science class. 

The goal of this project is to get data from [Box Office Mojo](https://www.boxofficemojo.com) and send an email weekly to my own email, with an HTML table showcasing the top 20 highest box office films of the week. 

Inside the requirements file, you will see the libraries that are required to run the code. 

In the Python folder, there are two files: `main.py` and `helper.py`. 

#### `main.py`
Here is the main Python code. There are 3 functions, in general, that construct the entire file: `mojo_weekly_scrape(weekly_website)` that gets the data from Box Office Mojo and stores them in a list of dictionaries, `weekly_html(listfOfDic)`that transfers the list of dictionaries to an HTML table using Jinja2, and `send_email(sender, receivers, appPassword, html_template)`that sends the email utilizing MIME objects. 

#### `helper.py`
Here is where the user enters the corresponding variables: the sender's email address, the receiver's email address, and the App Password to login to the sender's email account. 
## How to Use
### 1. Preparing the environment
When located to the directory, in command line type:

`pip install -r requirements.txt`

This will install all the libraries that are used in this project. 

### 2. Setting up email accounts
Open `helper.py`, and enter the email address for the `sender`and the `receivers`. You will also need to enter your `appPassword`, which is a password that apps can use to log into the sender's email account. 

You can find a tutorial on how to create an App Password for Gmail [here](https://www.lifewire.com/get-a-password-to-access-gmail-by-pop-imap-2-1171882).

You can enter multiple email addresses as a list for the `receivers` variable if you have multiple mailboxes that you would like to receive the email. 

### 3. Run the code! 
Run `main.py` and you will see the email in your mailbox in no time! 

### 4. Optional: Use Task Scheduler(for Windows system) to run the code every week.
You can utilize [task scheduler](https://www.tomsguide.com/how-to/how-to-use-task-scheduler-on-windows) to send an email to yourself every week! 
Using the bat file in the directory, schedule the task scheduler to run the bat file weekly. You can specify the environment and files to run using the bat file. 
*

*

*

*

*
## Disclaimer for Weekly Box Office Email
This project, titled "Weekly Box Office Email," is a personal, non-commercial project developed for educational/research purposes only.

### Data Source
The data used in this project has been sourced from [Box Office Mojo](https://www.boxofficemojo.com). This data is used under the premise of personal, non-commercial use, in alignment with Box Office Mojo's Terms of Use.

### No Affiliation
This project and its creator(s) are not affiliated, associated, authorized, endorsed by, or in any way officially connected with Box Office Mojo or any of its subsidiaries or its affiliates. The official Box Office Mojo website can be found at (https://www.boxofficemojo.com).

### Purpose
The primary purpose of this project is for the creator to learn computer science. This project is open-source and is intended for sharing coding practices, and techniques, and for educational purposes only.

### Copyright and Use
All content related to Box Office Mojo, including data, trademarks, etc., are the property of their respective owners. The use of Box Office Mojo's data in this project is solely for personal, educational, and non-commercial purposes.

### Changes to Disclaimer
This disclaimer may be updated or modified at any time. It is the responsibility of the users of this project to stay informed about any changes to this disclaimer.
