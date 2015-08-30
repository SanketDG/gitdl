#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_gitdl
----------------------------------
Tests for `gitdl` module.
"""

import os
import pytest

from gitdl import gitdl


class TestGitdl:

    def test_params_invalid_api_token(self):
        API_TOKEN = os.environ.get("GITDL")
        with pytest.raises(Exception):
            gitdl.get_params(API_TOKEN)

    def test_params_valid_api_token(self):
        API_TOKEN = os.environ.get("GITHUB_API_TOKEN")
        assert gitdl.get_params(API_TOKEN).get('API_TOKEN') == \
            os.environ.get("GITHUB_API_TOKEN")
