#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_gitdl
----------------------------------
Tests for `gitdl` module.
"""

import os
import pytest

import requests

from gitdl import gitdl


class TestGitdl:

    def test_params_invalid_api_token(self):
        API_TOKEN = os.environ.get("GITDL")
        with pytest.raises(Exception) as exc_info:
            gitdl.get_params(API_TOKEN)
        assert str(exc_info.value) == "GITHUB_API_TOKEN not found"

    def test_params_valid_api_token(self):
        API_TOKEN = os.environ.get("GITHUB_API_TOKEN")
        assert gitdl.get_params(API_TOKEN).get('API_TOKEN') == \
            os.environ.get("GITHUB_API_TOKEN")

    def test_get_first_search_result_invalid(self):
        url = "https://api.github.com/search/repositories?q=aksejake"
        response = requests.get(url).json()
        with pytest.raises(Exception) as exc_info:
            gitdl.get_first_search_result(response)
        assert str(exc_info.value) == "Repository Not Found."

    def test_download_exact_repo_invalid_repo(self):
        # does not contain the slash required for owner/repo format
        repo = "example"
        with pytest.raises(Exception) as exc_info:
            gitdl.download_exact_repo(repo)
        assert str(exc_info.value) == "Repository Not Found."
