# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-01-17 07:26:45
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-07-01 09:14:48

from .user_agent import UserAgent


def main():

    UA = UserAgent()
    print(UA.get_ua())


if __name__ == '__main__':
    main()
