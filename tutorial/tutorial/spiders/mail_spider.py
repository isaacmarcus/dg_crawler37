import os
import re
import sys
import pandas as pd
import scrapy
import requests
from lxml.html import fromstring
from googlesearch import search
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from email_validator import validate_email, EmailNotValidError
import phonenumbers as pn


class MailSpider(scrapy.Spider):
    name = 'email'

    def parse(self, response):

        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))

        for link in links:
            print(link)
            try:
                scrapy_request = scrapy.Request(url=link, callback=self.parse_link)
                scrapy_request.meta['dont_redirect'] = True
                scrapy_request.meta['handle_httpstatus_list'] = [302, 301]
                yield scrapy_request
            except Exception as e:
                print(e)

    def parse_link(self, response):

        for word in self.reject:
            if word in str(response.url):
                return

        reject_words_regex = ["career", "talent", "education", "someone", "yourname", "name", "example", "lastname",
                              "complain", ".jpg", ".png", "bootstrap", "vulnerability", "person", "akzonobel", "wixpress",
                              "email", "exemple"]
        try:
            html_text = str(response.text)
        except Exception as e:
            print(e)
        # regex parameters for searching for emails
        phone_list = re.findall('(?:\+65 [\d]{4} [\d]{4}|\+65[\d]{8}|[\d]{4} [\d]{4}||[\d]{8})+', html_text)
        mail_list = re.findall('(?!.*\w{1}\.\w{1}\.\w{1})(?!.*\.google\.com)(?:(\w+@\w+\.[\w+\.{1}]+))+', html_text)
        # empty lists to add valid email and phone numbers to
        newPhoneList = []
        newMailList = []
        # only loop through is mail list is not empty
        if len(mail_list) > 0:
            for i in range(len(mail_list)):
                # change mail item to lowercase
                mail_list[i] = mail_list[i].lower()
                # loop through reject words list
                reject_found = False
                for word in reject_words_regex:
                    # if word is found in email, remove it and all instances of it from list
                    if str(word.lower()) in str(mail_list[i].lower()):
                        reject_found = True
                        # mail_list = list(filter(mail_list[i].__ne__, mail_list))
                # double check if valid email format
                try:
                    validEmail = validate_email(mail_list[i])
                    mail_list[i] = validEmail.ascii_email
                    # append to new list if no reject word found, not already in list and is a valid email
                    if not reject_found and mail_list[i] not in newMailList:
                        newMailList.append(validEmail.ascii_email)
                except Exception as e:
                    print(e)
                    # if not valid, don't add to new list
                    # mail_list = list(filter(mail_list[i].__ne__, mail_list))

        # check if phone list is empty
        if len(phone_list) > 0:
            for numberIndex in range(len(phone_list)):
                parsedNumber = pn.parse(phone_list[numberIndex], region='SG')
                if pn.is_valid_number(parsedNumber) and phone_list[numberIndex] not in newPhoneList:
                    newPhoneList.append(phone_list[numberIndex])

        # add dictiionary of emails and numbers to csv
        phonedic = {'phone': newPhoneList, 'link': str(response.url)}
        maildic = {'email': newMailList, 'link': str(response.url)}
        maildf = pd.DataFrame(maildic)
        maildf.to_csv("mail_" + self.path, mode='a', header=False)
        phonedf = pd.DataFrame(phonedic)
        phonedf.to_csv("ph_" + self.path, mode='a', header=False)


def get_proxies():
    proxy_url = "https://www.proxynova.com/proxy-server-list/elite-proxies/"
    proxy_file = open("proxy_list.txt", "w+")
    proxy_response = requests.get(proxy_url)
    parser = fromstring(proxy_response.text)
    output = set()
    for i in parser.xpath('//tbody/tr'):
        # if i.xpath('.//td[1]/abbr/script[contains(text())]'):
        try:
            cur_proxy = ":".join([re.search("(\d+\.\d+\.\d+\.\d+)", str(i.xpath('.//td[1]/abbr/script/text()')[0].strip())).group(), i.xpath('.//td[2]/text()')[0].strip()])
            proxy_file.write(cur_proxy + "\n")
            output.add(cur_proxy)
        except Exception as e:
            print(e)
    proxy_file.close()
    return output


def get_urls(tag, n, language):
    urls = [url for url in search(tag, stop=n, lang=language, country="countrySG")][:n]
    return urls


def ask_user(question):
    response = input(question + ' y/n' + '\n')
    if response == 'y':
        return True
    else:
        return False


def create_file(path):
    response = False
    if os.path.exists(path):
        response = ask_user('File already exists, replace?')
        if not response:
            return

    with open(path, 'wb') as file:
        file.close()


def get_info(tag, n, language, path, reject=[]):
    create_file("mail_" + path)
    df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df.to_csv("mail_" + path, mode='w', header=True)
    phdf = pd.DataFrame(columns=['phone', 'link'], index=[0])
    phdf.to_csv("ph_" + path, mode='w', header=True)

    print('Collecting proxies...')
    get_proxies()

    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)

    print('Searching for emails...')
    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
    process = CrawlerProcess()
    process.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
    process.start()

    print('Cleaning emails...')
    df = pd.read_csv("mail_" + path, index_col=0)
    df.columns = ['email', 'link']
    df = df.drop_duplicates(subset='email')
    df = df.reset_index(drop=True)
    df.to_csv("mail_" + path, mode='w', header=True)

    phdf = pd.read_csv("ph_" + path, index_col=0)
    phdf.columns = ['phone', 'link']
    phdf = df.drop_duplicates(subset='phone')
    phdf = df.reset_index(drop=True)
    phdf.to_csv("ph_" + path, mode='w', header=True)

    process.stop()

    return df


def file_namer(search_term):
    output = ""
    for word in search_term.split():
        output += word.lower()
        output += "_"
    output = output[:-1] + ".csv"
    return output


key = "AIzaSyAv8Cbe7A-tlSfEwLDwo7romFPRj7vXD2Y"
search_param = "Singapore Pharmaceuticals Contact"
# Incomplete: Chemicals Industry Contacts
csv_path = "paints_coatings.csv"
reject_words = ["facebook", "wikipedia", "twitter", 'wiki', 'youtube', "flickr", "instagram", "imgur", "jobscentral",
                "jobstreet", "linkedin", "straitstimes", "channelnewsasia", "sphsubscription", "todayonline", "asiaone",
                "singaporenews", "mothership", "theindependent", "career", "careers", "pdf", "shell", "taleo"]
search_terms = ["Singapore Pharmaceuticals Contact", "Aerospace Contact", "Paints and Coatings Contact", "Chemicals Industry Contact",
                "Optical Coatings Contacts", "Medical Apparatus Manufacturer Contact"]

get_info(search_param, 50, 'en', file_namer(search_param), reject=reject_words)

# df = pd.read_csv(csv_path, index_col=0)
# df.columns = ['email', 'link']
# df = df.drop_duplicates(subset='email')
# df = df.reset_index(drop=True)
# df.to_csv(csv_path, mode='w', header=True)


# supply chain manager contact
