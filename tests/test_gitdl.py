#!/usr/bin/env python

"""
test_gitdl
----------------------------------
Tests for `gitdl` module.
"""

import json
import os
import unittest

import pytest

from mock import patch

import requests
import requests_mock

from gitdl import gitdl


class TestGitdl(unittest.TestCase):

    def test_params_invalid_api_token(self):
        with patch.dict('os.environ', {}):
            API_TOKEN = os.environ.get("RANDOM-KEY")
        with pytest.raises(Exception) as exc_info:
            gitdl.get_params(API_TOKEN)
        assert str(exc_info.value) == "GITHUB_API_TOKEN not found"

    def test_params_valid_api_token(self):
        with patch.dict('os.environ', {"GITHUB_API_TOKEN": "key123"}):
            API_TOKEN = os.environ.get("GITHUB_API_TOKEN")
            assert gitdl.get_params(API_TOKEN).get('API_TOKEN') == \
                os.environ.get("GITHUB_API_TOKEN")

    def test_get_first_search_result_invalid(self):
        fake_json = json.dumps({'items': []})
        url = "https://api.github.com/search/repositories?q=aksejake"
        with requests_mock.mock() as mocker:
            mocker.get(url, json=fake_json)
            response = json.loads(requests.get(url).json())
        with pytest.raises(Exception) as exc_info:
            gitdl.get_first_search_result(response)
        assert str(exc_info.value) == "Repository Not Found."

    def test_download_exact_repo_invalid_repo(self):
        # does not contain the slash required for owner/repo format
        repo = "example"
        with requests_mock.mock() as mocker:
            mocker.get("https://api.github.com/repos/{}".format(repo),
                       status_code=404)
            with pytest.raises(Exception) as exc_info:
                gitdl.download_exact_repo(repo)
            assert str(exc_info.value) == "Repository Not Found."

    def test_get_size(self):
        with requests_mock.mock() as mocker:
            mocker.get("mock://google.com",
                       headers={'Content-Length': '42'})
            r = requests.get("mock://google.com")
        self.assertEqual(gitdl.get_size(r), 0.04)

    def test_get_search_results(self):
        with requests_mock.mock() as mocker:
            mocker.get("https://api.github.com/search/repositories?"
                       "q=gitdl&sort=&order=desc&per_page=30",
                       json="Found 3 repos!")
            resp = gitdl.get_search_results("gitdl")
        self.assertEqual(resp, "Found 3 repos!")

    def test_get_first_search_result_valid(self):
        fake_json = json.dumps({'items': [{"id": 1, "name": "gitdl"}]})
        url = "https://api.github.com/search/repositories?q=aksejake"
        with requests_mock.mock() as mocker:
            mocker.get(url, json=fake_json)
            response = json.loads(requests.get(url).json())
        res = gitdl.get_first_search_result(response)
        self.assertEqual(res, {'id': 1, 'name': 'gitdl'})

    def test_get_repo_names(self):
        url = "https://api.github.com/search/repositories?q=anything"
        fake_json = json.dumps(
            {'items': [{'id': 1, 'full_name': 'SanketDG/gitdl'},
                       {'id': 2, 'full_name': 'SanketDG/djurl'}]})
        with requests_mock.mock() as mocker:
            mocker.get(url, json=fake_json)
            response = json.loads(requests.get(url).json())
        res = gitdl.get_repo_names(response)
        self.assertEqual(res, ['SanketDG/gitdl', 'SanketDG/djurl'])

    def test_get_search_results_first_only(self):
        fake_json = {'items': [{"id": 1, "name": "gitdl"}]}
        with requests_mock.mock() as mocker:
            mocker.get("https://api.github.com/search/repositories?"
                       "q=gitdl&sort=&order=desc&per_page=30",
                       json=fake_json)
            resp = gitdl.get_search_results("gitdl", only_first=True)
        self.assertEqual(resp, {'id': 1, 'name': 'gitdl'})
