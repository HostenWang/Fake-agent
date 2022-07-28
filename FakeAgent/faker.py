# Copyright (c) 2022 Itz-fork
import os
import requests

from enum import Enum
from json import loads
from random import choice
from .types import Browsers


class Fake_Agent:
    """
    Fake_Agent class

    ### Arguments

        - `browser` :Enum (optional) - Enum of the rowser that you want to use (from FakeAgent.types import Browsers)
        - `load_on_init` :bool (optional) - Whether you want to load json file to memory on init
    """

    def __init__(self, browser: Enum = Browsers.FIREFOX, load_on_init: bool = True) -> None:
        self.browser = browser
        # Json file
        self.json_file = None
        if load_on_init:
            self.json_file = self._read_json_as_dict(
                f"{os.path.dirname(__file__)}/data/{self.browser.value}.json")

    def get(self, browser: Enum = None, as_gen: bool = False):
        """
        Get user agents as a list or generator according to the browser that Fake_Agent class initialized with

        ### Arguments

            - `browser` :Enum (optional) - Pass Browser enum if you want to get user agents of a specific browser rather than the one you initialized the Fake_Agent class with
            - `as_gen` :bool (optional) - Pass "True" if you want to return value as a generator rather than a list
        """
        to_use = browser.value if browser else self.browser.value
        vl = self.json_file if self.json_file else self._read_json_as_dict(
            f"{os.path.dirname(__file__)}/data/{to_use}.json")
        if as_gen:
            return (val for val in vl.values())
        else:
            return [val for val in vl.values()]

    def chrome(self, as_gen: bool = False):
        """
        Get chrome user agents as a list or generator

        ### Arguments

            - `as_gen` :bool (optional) - Pass "True" if you want to return value as a generator rather than a list
        """
        return self.get(Browsers.CHROME, as_gen)

    def firefox(self, as_gen: bool = False):
        """
        Get firefox user agents as a list or generator

        ### Arguments

            - `as_gen` :bool (optional) - Pass "True" if you want to return value as a generator rather than a list
        """
        return self.get(Browsers.FIREFOX, as_gen)

    def edge(self, as_gen: bool = False):
        """
        Get edge user agents as a list or generator

        ### Arguments

            - `as_gen` :bool (optional) - Pass "True" if you want to return value as a generator rather than a list
        """
        return self.get(Browsers.EDGE, as_gen)

    def opera(self, as_gen: bool = False):
        """
        Get opera user agents as a list or generator

        ### Arguments

            - `as_gen` :bool (optional) - Pass "True" if you want to return value as a generator rather than a list
        """
        return self.get(Browsers.OPERA, as_gen)

    def safari(self, as_gen: bool = False):
        """
        Get safari user agents as a list or generator

        ### Arguments

            - `as_gen` :bool (optional) - Pass "True" if you want to return value as a generator rather than a list
        """
        return self.get(Browsers.SAFARI, as_gen)

    def internet_explorer(self, as_gen: bool = False):
        """
        Get internet explorer user agents as a list or generator

        ### Arguments

            - `as_gen` :bool (optional) - Pass "True" if you want to return value as a generator rather than a list
        """
        return self.get(Browsers.IE, as_gen)

    def random(self, mix_browsers: bool = True, with_details: bool = False):
        """
        Randomly select user agent

        ### Arguments

            - `mix_browsers` :bool (optional) - Pass "True" if you want to randomly select browser too
            - `with_details` :bool (optional) - Pass "True" if you need to get user agent details (INTERNET REQUIRED)
        """
        us_brw = choice(self._get_supported_browsers()
                        ) if mix_browsers else self.browser.value
        brdict = self.json_file if self.json_file else self._read_json_as_dict(
            f"{os.path.dirname(__file__)}/data/{us_brw}.json")
        chosen = choice(list(brdict.values()))
        return self._get_ua_data(chosen) if with_details else chosen

    def _get_supported_browsers(self):
        return [v.value for k, v in Browsers.__dict__.items() if k.isupper()]

    def _get_ua_data(self, ua):
        resp = requests.get(
            f"http://useragentstring.com/?uas={ua}&getJSON=all").json()
        resp["agent"] = ua
        return resp

    def _read_json_as_dict(self, path: str) -> dict:
        with open(path, "r") as r:
            return loads(r.read())
