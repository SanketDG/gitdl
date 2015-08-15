import requests
import os
import zipfile
import sys

API_TOKEN = os.environ.get('GITHUB_API_TOKEN')


def get_params():
    """Set parameters of the request"""
    if API_TOKEN is None:
        raise Exception('GITHUB_API_TOKEN not found')
    params = {'API_TOKEN': API_TOKEN}  # create a dict to be passed by request
    return params


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


def get_first_search_result(resp):
    "Gets first search result from json response"
    try:
        first_result = resp['items'][0]
        return first_result
    except IndexError:
        print("No such repository exists.")
        exit(1)


def work_them_files(repo_name):
    "Extract, rename and delete."
    extractfiles("{}.zip".format(repo_name))
    os.rename("{}-master".format(repo_name), "{}".format(repo_name))
    os.unlink("{}.zip".format(repo_name))


def main():
    # send a GET to search url in GitHub API
    url = "https://api.github.com/search/repositories?q={}".format(sys.argv[1])
    response = requests.get(url, params=get_params()).json()

    first_result = get_first_search_result(response)  # check for empty response

    download_url = first_result['html_url'] + '/archive/master.zip'
    repo_name = first_result['name']  # stores the repository name
    print(download_url)

    urlretrieve(download_url, "{}.zip".format(repo_name))

    work_them_files(repo_name)


if __name__ == "__main__":
    main()
