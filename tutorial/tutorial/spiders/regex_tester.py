import re
import phonenumbers as pn
import pandas as pd

html_text = 'info@clariant.com \n info@infocentric.research.com \n icons@2.4.1 \n service@hispaint.com \n bla@calendar.google.com' \
            '\n +65 9678 1723 \n +6598769876 \n 9876 5432 \n 1234 5678 \n 12345678 \n 87654321 \n 98765432 \n 6598765433'
mail_list = re.findall('(?!.*\w{1}\.\w{1}\.\w{1})(?!.*\.google\.com)(?:(\w+@\w+\.[\w+\.{1}]+))+', html_text)

phone_list = re.findall('(?:\+65 [\d]{4} [\d]{4}|\+65[\d]{8}|[\d]{4} [\d]{4}|[\d]{8})+', html_text)

for mail in mail_list:
    print(mail)

newPhoneList = []

for numberIndex in range(len(phone_list)):
    parsedNumber = pn.parse(phone_list[numberIndex], region='SG')
    if pn.is_valid_number(parsedNumber) and phone_list[numberIndex] not in newPhoneList:
        newPhoneList.append(phone_list[numberIndex])

loldic = {'phone': phone_list, 'link' : str("this is the url")}
dicdic = {'email': newPhoneList, 'link': str("this is the url")}
maildf = pd.DataFrame(dicdic)
phonedf = pd.DataFrame(loldic)
print(phonedf)
newdf = maildf.join(phonedf)
print(newdf)
