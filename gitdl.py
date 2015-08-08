import urllib
from pprint import pprint
import requests
import json

params = dict(API_TOKEN="61552c37f3ffd44bbe6a3473779895b3d3f2340b")

url = "https://api.github.com/search/repositories?q={}".format(input())


def main():
    # request = urllib.request.Request(url)
    # request.add_header('Authorization', 'token %s' % API_TOKEN)
    response = requests.get(url, params=params).text
    search_results = json.loads(response)
    download_url = search_results['items'][0]['html_url'] + '/archive/master.zip'
    print(download_url)
    urllib.request.urlretrieve(download_url, "{}.zip".format(search_results['items'][0]['name']))
    print("SAVED")

if __name__ == "__main__":
    main()
