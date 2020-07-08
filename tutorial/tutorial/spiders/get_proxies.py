# from lxml.html import fromstring
# import requests
# from itertools import cycle
# import traceback
# import re
#
# proxy_link = "https://www.proxynova.com/proxy-server-list/elite-proxies/"
# # proxy_file_list = []
#
# # def get_proxies():
# #     proxy_file = open("proxy_list.txt", "w+")
# #     proxy_url = 'https://free-proxy-list.net/'
# #     proxy_response = requests.get(proxy_url)
# #     parser = fromstring(proxy_response.text)
# #     output = set()
# #     for i in parser.xpath('//tbody'):
# #         if i.xpath('.//tr/td[1][contains(text(),"yes")]'):
# #             cur_proxy = ":".join([i.xpath('.//tr/td[1]/text()')[0], i.xpath('.//tr/td[2]/text()')[0]])
# #             proxy_file.write(cur_proxy + "\n")
# #             print(cur_proxy)
# #             output.add(cur_proxy)
# #     proxy_file.close()
# #     return output
#
#
# def get_proxies():
#     proxy_url = proxy_link
#     proxy_file = open("proxy_list.txt", "w+")
#     proxy_response = requests.get(proxy_url)
#     parser = fromstring(proxy_response.text)
#     output = set()
#     for i in parser.xpath('//tbody/tr')[:10]:
#         cur_proxy = ":".join([re.search("(\d+\.\d+\.\d+\.\d+)", str(i.xpath('.//td[1]/abbr/script/text()')[0].strip())).group(), i.xpath('.//td[2]/text()')[0].strip()])
#         proxy_file.write(cur_proxy + "\n")
#         output.add(cur_proxy)
#     proxy_file.close()
#     return output
#
#
# #If you are copy pasting proxy ips, put in the list below
# #proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
# proxies = get_proxies()
# # print(proxies)
# open_file = open("proxy_list.txt", "r")
# proxy_list = set()
# for i in open_file.readlines():
#     print(i.strip())
#     if i != "":
#         proxy_list.add(i)
# # print(proxy_list)
# proxy_pool = cycle(proxy_list)
#
# url = 'https://httpbin.org/ip'
# for i in range(1, 15):
#     #Get a proxy from the pool
#     proxy = next(proxy_pool)
#     print("Request #%d"%i)
#     try:
#         response = requests.get(url, proxies={"http": proxy, "https": proxy})
#         print(response.json())
#     except:
#         #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
#         #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
#         print("Skipping. Connnection error")