import re

html_text = 'info@clariant.com \n info@infocentric.research.com \n icons@2.4.1 \n service@hispaint.com \n bla@calendar.google.com'
mail_list = re.findall('(?!.*\w{1}\.\w{1}\.\w{1})(?!.*\.google\.com)(?:(\w+@\w+\.[\w+\.{1}]+))+', html_text)

for mail in mail_list:
    print(mail)
