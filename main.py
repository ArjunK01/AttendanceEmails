import pandas as pd
import requests
import csv
import datetime

import sendgrid
import os
from sendgrid.helpers.mail import *

xl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRG_-yGq3ZPVOhAHSU3uhO8q2zZNopiNaY07BDckKpU0wzLPNhgRa2ruWrkkdItUv-cf2LnU-iRV51L/pub?output=xlsx"

data = pd.ExcelFile(xl)

classes = ['Token', 'Wireframe', 'Node', 'Source', 'Source Pro', 'Source Lite', 'Quantify', 'Convert']

dates = {
    "Source": [
        datetime.datetime(2022, 2, 14),
        datetime.datetime(2022, 2, 15),
        datetime.datetime(2022, 2, 20),
        datetime.datetime(2022, 3, 13),
        datetime.datetime(2022, 3, 20),
        datetime.datetime(2022, 3, 27),
        datetime.datetime(2022, 4, 3),
        datetime.datetime(2022, 4, 10),
        datetime.datetime(2022, 4, 17),
    ],

}

def get_last_workshop(className):
    past_workshop = 0
    now = datetime.datetime.now()
    for x in range(len(dates[className])):
        if dates[className][x]< now:
            past_workshop = "W"+str(x+1)+" Workshop"
    print(past_workshop)
    return past_workshop

def get_missed_students(attendence_data, student_info): 
    missed = []
    for x in range(len(attendence_data)):
        if attendence_data[x][0]==0:
            missed.append(list(student_info[x]))
    return missed

def send_email(className, personInfo):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("arjun@joinforge.co")
    cc_email = Email("ak7cw@virginia.edu")
    p = Personalization()
    p.add_to(cc_email)
    to_email = To(personInfo[2])
    subject = className + " Missing Workshop"
    content = Content("text/plain", f"Hey {personInfo[0]},\n\nIf you’re receiving this, then according to our records you didn’t come to workshop this week. (If we’re wrong on this, let us know!)\nIf you’re no longer interested in Source, we’d love to know why and if there’s anything we can do to improve your experience! We welcome any and all feedback.\nIf you had extenuating circumstances, please let us know, too. Life happens, and we understand, but we want to know that you are still interested in continuing with Source.\nLet us know. Thank you!\n\nBest,\nArjun Kumar - Source PL")
    mail = Mail(from_email, to_email, subject, content)
    mail.add_personalization(p)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response)

def send_emails(className):
    class_info = pd.read_excel(data, className)
    past_workshop = get_last_workshop(className)

    attendence_data = class_info[[past_workshop]].to_numpy()
    student_info = class_info[["Student FN", "Student LN", "Student Email"]].to_numpy()

    missed = get_missed_students(attendence_data, student_info)

    send_email("Source", ["Arjun", "Kumar", "ak7cw@virginia.edu"])
    for x in missed:
        # send_email("Source", x)
        print(x)



send_emails("Source")