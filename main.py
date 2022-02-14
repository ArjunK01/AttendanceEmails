import pandas as pd
import requests
import csv
import datetime

CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRG_-yGq3ZPVOhAHSU3uhO8q2zZNopiNaY07BDckKpU0wzLPNhgRa2ruWrkkdItUv-cf2LnU-iRV51L/pub?gid=1186908515&single=true&output=csv'

data = pd.read_csv(CSV_URL)

source_dates = [
    datetime.datetime(2022, 2, 14),
    datetime.datetime(2022, 2, 20),
    datetime.datetime(2022, 3, 13),
    datetime.datetime(2022, 3, 20),
    datetime.datetime(2022, 3, 27),
    datetime.datetime(2022, 4, 3),
    datetime.datetime(2022, 4, 10),
    datetime.datetime(2022, 4, 17),
    datetime.datetime(2022, 4, 24),
]


past_workshop = 0
now = datetime.datetime.now()
for x in range(len(source_dates)):
    if source_dates[x]< now:
        past_workshop = "W"+str(x+1)+" Workshop"


attendence_data = data[[past_workshop]].to_numpy()
student_info = data[["Student FN", "Student LN", "Student Email"]].to_numpy()

missed = []
for x in range(len(attendence_data)):
    if attendence_data[x][0]=='0':
        missed.append(list(student_info[x]))

print(missed)





