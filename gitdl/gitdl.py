import requests
import json
import os
import zipfile

API_TOKEN = os.environ.get('GITHUB_API_TOKEN')
params = {'API_TOKEN': API_TOKEN}  # create a dict to be passed by the request

url = "https://api.github.com/search/repositories?q={}".format(input())


def urlretrieve(url, path):
    """Retrieves a zipfile and writes it to a local disk"""
    with open(path, 'wb') as f:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(1024):
            f.write(chunk)


def extractfiles(zipf):
    """Extract a zipfile to the current directory"""
    with zipfile.ZipFile(zipf, "r") as z:
        z.extractall()


def main():
    response = requests.get(url, params=params).text
    search_results = json.loads(response)
    first_result = search_results['items'][0]  # takes out the first result
    download_url = first_result['html_url'] + '/archive/master.zip'
    repo_name = first_result['name']  # stores the repository name
    print(download_url)
    urlretrieve(download_url, "{}.zip".format(repo_name))
    extractfiles("{}.zip".format(repo_name))
    os.rename("{}-master".format(repo_name), "{}".format(repo_name))
    os.unlink("{}.zip".format(repo_name))

if __name__ == "__main__":
    main()
