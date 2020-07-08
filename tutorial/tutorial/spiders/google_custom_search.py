from googleapiclient.discovery import build

my_cse_id = "014543770622701713752:wgz8l--o4n4"
dev_key = "AIzaSyAv8Cbe7A-tlSfEwLDwo7romFPRj7vXD2Y"


def google_search(search_term, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=dev_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


results = google_search('Chemicals Industry Contact', my_cse_id, num=10, cr="countrySG", lr="lang_en")
for result in results:
    print(result.get('link'))

for i in range(10):
    print("number " + str(i))