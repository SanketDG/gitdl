"""

gitdl - download github repositories easily!

Arguments:
   REPO   Repository to download

Usage:
  gitdl search <REPO> [--sort <field> ( --asc | --desc )]
  gitdl <REPO>
  gitdl -h | --help
  gitdl --version

 Options:
   -h --help    Show this message.
   --version    Show version
"""

import requests
import os
import zipfile
from docopt import docopt
from . import __version__

API_TOKEN = os.environ.get('GITHUB_API_TOKEN')


def get_params(API_TOKEN):
    """
    Set parameters of the request using GITHUB_API_TOKEN environment variable
    """
    if API_TOKEN is None:
        raise Exception('GITHUB_API_TOKEN not found')
    params = {'API_TOKEN': API_TOKEN}  # create a dict to be passed by request
    return params


def urlretrieve(url, path):
    """
    Retrieves a zipfile and writes it to a local disk
    """
    with open(path, 'wb') as f:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(1024):
            f.write(chunk)


def extractfiles(zipf):
    """
    Extract a zipfile to the current directory
    """
    with zipfile.ZipFile(zipf, "r") as z:
        z.extractall()


def get_first_search_result(resp):
    """
    Gets first search result from json response
    """
    try:
        first_result = resp['items'][0]
        return first_result
    except IndexError:
        raise Exception("Repository Not Found.")


def work_them_files(repo_name):
    """
    Extract, rename and delete.
    """
    extractfiles("{}.zip".format(repo_name))
    os.rename("{}-master".format(repo_name), "{}".format(repo_name))
    os.unlink("{}.zip".format(repo_name))


def get_repo_names(response):
    items = response['items']
    repo_names = [item['name'] for item in items]
    return repo_names


def get_search_results(search_term, sort_field="", sort_order="desc",
                       only_first=False):
    # send a GET to search url in GitHub API
    url = "https://api.github.com/search/repositories? \
            q={}&sort={}&order={}".format(search_term, sort_order, sort_field)
    response = requests.get(url, params=get_params(API_TOKEN)).json()
    if only_first:
        result = get_first_search_result(response)
    else:
        # fetch results
        result = get_repo_names(response)
    return result


def main():

    args = docopt(__doc__, version=__version__)

    repo = args['<REPO>']
    # if search is used, then print the results
    if args['search']:
        sort_order = 'asc' if args.get('asc') else 'desc'
        if args['--sort']:
            sort_field = args['<field>']
        results = get_search_results(repo, sort_order, sort_field)

        for result in results:
            print(result)
    else:
        first_result = get_search_results(repo, only_first=True)

        download_url = first_result['html_url'] + '/archive/master.zip'
        repo_name = first_result['name']  # stores the repository name
        print(download_url)

        urlretrieve(download_url, "{}.zip".format(repo_name))

        work_them_files(repo_name)


if __name__ == "__main__":
    main()
