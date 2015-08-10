import requests
import json
import os
import zipfile

API_TOKEN = os.environ.get('GITHUB_API_TOKEN')
params = {'API_TOKEN': API_TOKEN}

url = "https://api.github.com/search/repositories?q={}".format(input())


def urlretrieve(url, path):
    with open(path, 'wb') as f:
        r = requests.get(url, stream=True)
        r.raise_for_status()  # Replace this with better error handling.

        for chunk in r.iter_content(1024):
            f.write(chunk)


def extractfiles(zipf):
    with zipfile.ZipFile(zipf, "r") as z:
        z.extractall()


def main():
    # request = urllib.request.Request(url)
    # request.add_header('Authorization', 'token %s' % API_TOKEN)
    response = requests.get(url, params=params).text
    search_results = json.loads(response)
    first_result = search_results['items'][0]
    download_url = first_result['html_url'] + '/archive/master.zip'
    repo_name = first_result['name']
    print(download_url)
    urlretrieve(download_url, "{}.zip".format(repo_name))
    extractfiles("{}.zip".format(repo_name))
    os.rename("{}-master".format(repo_name), "{}".format(repo_name))
    os.unlink("{}.zip".format(repo_name))

if __name__ == "__main__":
    main()
