from urllib.request import urlretrieve
import requests
import json
import os

params = dict(API_TOKEN=os.environ.get('GITHUB_API_TOKEN'))

url = "https://api.github.com/search/repositories?q={}".format(input())


def main():
    # request = urllib.request.Request(url)
    # request.add_header('Authorization', 'token %s' % API_TOKEN)
    response = requests.get(url, params=params).text
    search_results = json.loads(response)
    first_result = search_results['items'][0]
    download_url = first_result['html_url'] + '/archive/master.zip'
    print(download_url)
    urlretrieve(download_url, "{}.zip".format(first_result['name']))
    print("{}.zip saved in {}".format(first_result['name'], os.getcwd()))

if __name__ == "__main__":
    main()
