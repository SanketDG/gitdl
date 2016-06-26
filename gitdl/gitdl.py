"""

gitdl - download github repositories easily!

Arguments:
   REPO   Repository to download

Usage:
  gitdl search <REPO> [--sort <sort_field> ( --asc | --desc )]
  gitdl search <REPO> [--per_page <display>]
  gitdl <REPO> [-e]
  gitdl -h | --help
  gitdl --version

 Options:
   -e, --exact  Download exact repository
   -h, --help   Show this message.
   -v, --version    Show version
"""

import os
import requests
import zipfile

from docopt import docopt
from tabulate import tabulate
from tqdm import tqdm

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


def get_size(request):
    """
    Retrieves a size of a request object in KB.
    """
    # get the 'Content-Length' response and convert it to int
    size = int(request.headers.get('Content-Length'))
    # convert bytes to KB
    size /= 1024
    # round to two decimal places
    size = round(size, 2)
    return size


def urlretrieve(url, path):
    """
    Retrieves a zipfile and writes it to a local disk
    """
    with open(path, 'wb') as f:
        r = requests.get(url, stream=True)
        for chunk in tqdm(r.iter_content(1024), unit='k',
                          total=get_size(r), ncols=100):
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


def work_them_files(repo_name, branch):
    """
    Extract, rename and delete.
    """
    extractfiles("{}.zip".format(repo_name))
    os.rename("{}-{}".format(repo_name, branch), "{}".format(repo_name))
    os.unlink("{}.zip".format(repo_name))


def get_repo_names(response):
    items = response['items']
    repo_names = [item['full_name'] for item in items]
    return repo_names


def get_search_results(search_term, sort_field="", sort_order="desc",
                       per_page=30, only_first=False):
    # send a GET to search url in GitHub API
    url = ("https://api.github.com/search/repositories?"
           "q={}&sort={}&order={}&per_page={}".format(search_term, sort_field,
                                                      sort_order,
                                                      str(per_page)))
    print(url)
    response = requests.get(url, params=get_params(API_TOKEN)).json()
    if only_first:
        result = get_first_search_result(response)
        return result
    else:
        # return the whole json
        return response


def download_zip_and_extract(repo_json):
    default_branch = repo_json['default_branch']
    download_url = "{}/archive/{}.zip".format(
        repo_json['html_url'], default_branch)
    repo_name = repo_json['name']  # stores the repository name
    print(download_url)

    urlretrieve(download_url, "{}.zip".format(repo_name))

    work_them_files(repo_name, default_branch)


def download_exact_repo(repo):
    url = "https://api.github.com/repos/{}".format(repo)
    response = requests.get(url, params=get_params(API_TOKEN))
    if response.status_code == 404:
        raise Exception("Repository Not Found.")
    response = response.json()
    download_zip_and_extract(response)


def tabulate_view(search_results):
    table = []
    # headers for the table
    headers = ['Name', 'Stars', 'Forks', 'Language', 'Last Updated']
    # loop through each of the items containing the repo data
    for repo_data in search_results["items"]:

        # collect necessary data
        repo_name = repo_data['full_name']
        repo_stars = repo_data['stargazers_count']
        repo_forks = repo_data['forks_count']
        repo_language = repo_data['language']
        updated_at = repo_data['pushed_at']

        repo_row = [
            repo_name, repo_stars, repo_forks,
            repo_language, updated_at
        ]

        table.append(repo_row)

    # display in tabulate format
    print(tabulate(table, headers, tablefmt="grid"))


def main():

    args = docopt(__doc__, version=__version__)

    repo = args['<REPO>']
    # if search is used, then print the results
    if args['search']:
        sort_order = 'asc' if args.get('--asc') else 'desc'
        sort_field = args['<field>'] if args['--sort'] else ""
        per_page = args['<display>'] if args['--per_page'] else ""
        results = get_search_results(repo, sort_field, sort_order, per_page)

        tabulate_view(results)
    elif args["--exact"]:
        download_exact_repo(repo)
    else:
        first_result = get_search_results(repo, only_first=True)
        download_zip_and_extract(first_result)


if __name__ == "__main__":
    main()
