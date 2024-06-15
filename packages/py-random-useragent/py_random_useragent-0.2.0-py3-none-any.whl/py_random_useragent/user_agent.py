# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg <olegsuvorinov@me.com>
# @Date:   2023-02-28 10:01:30
# @Last Modified by:   Suvorinov Oleg
# @Last Modified time: 2024-06-14 13:03:52

import random

import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

U_A = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0' # noqa


class UserAgent(object):
    """docstring for UserAgent"""

    def __init__(self):
        super(UserAgent, self).__init__()

        self._u_agents = []
        self.__most_common_user_agents()

    def __most_common_user_agents(self):
        """Забираем c https://cdn.suvorinov.ru/user_agents/user_agents.txt
        Огромное спасибо Мне"""

        sess = requests.session()
        cached_sess = CacheControl(sess, cache=FileCache('.web_cache'))

        try:
            r = cached_sess.get('https://cdn.suvorinov.ru/user_agents/user_agents.txt') # noqa
            self._u_agents = r.text.split('\n')[:-1]
        except Exception:
            pass

    def get_ua(self) -> str:
        if self._u_agents:
            return random.choice(self._u_agents)
        return U_A
