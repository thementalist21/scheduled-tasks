# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import pandas as pd
import smtplib
import random
from datetime import datetime
import os

# Configuration
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")  # Use an App Password, not your login password
TEMPLATES = ["letter_1.txt", "letter_2.txt"]

# 1. Check if today matches any birthday
today = datetime.now()
today_tuple = (today.month, today.day)
df = pd.read_csv("birthdays.csv")

for index, row in df.iterrows():
    birthday_tuple = (int(row['month']), int(row['day']))
    
    if today_tuple == birthday_tuple:
        # 2. Select a random template and replace the placeholder
        file_path = f"letter_templates/{random.choice(TEMPLATES)}"
        with open(file_path) as letter_file:
            contents = letter_file.read()
            # Replace [NAME] with the actual name from the CSV
            contents = contents.replace("[NAME]", row["name"])

        # 3. Send the email via SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # Secure the connection
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=row["email"],
                msg=f"Subject:Happy Birthday!\n\n{contents}"
            )
        print(f"Birthday email sent to {row['name']}!")
