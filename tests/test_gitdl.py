#!/usr/bin/env python

"""
test_gitdl
----------------------------------
Tests for `gitdl` module.
"""

import json
import os

import pytest

from mock import patch

import requests
import requests_mock

from gitdl import gitdl


class TestGitdl:

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
