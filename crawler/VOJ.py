# -*- coding: utf-8 -*-

import os
import sys
import requests
from generic_crawler import GenericCrawler


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../code/VOJ')
BASE_URL = 'https://vn.spoj.com/'


class VojCrawler(object, GenericCrawler):
    def __init__(self):
        GenericCrawler.__init__(
            self,
            BASE_URL,
            BASE_URL + 'users/{}/',
            BASE_URL + 'status/{},{}/',
            BASE_URL + 'files/src/save/{}',
            '<a href="/status/[^,]+,{}/">(?P<id>.+)</a>',
            '.*(Đạt yêu cầu|Accepted|100)',
            '.*href="/files/src/(?P<id>\d+)/'
        )

    def login(self, session, username, password):
        super(VojCrawler, self)._login(session, data={
            'login_user': username,
            'password': password
        })


def main(crawler, output_dir):
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
        if len(sys.argv) >= 4:
            output_dir = sys.argv[3]
    else:
        username = raw_input('Your username: ')
        password = raw_input('Your password: ')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    session = requests.Session()
    crawler.login(session, username, password)

    problems = crawler.get_solved_problems(session, username)
    print '{} has solved {} problems'.format(username, len(problems))

    for problem in problems:
        for extension in ['java', 'cpp', 'py', 'pas']:
            if os.path.isfile(os.path.join(output_dir, problem + '.' + extension)):
                break
        else:
            crawler.download_solution(session, output_dir, username, problem)


if __name__ == '__main__':
    crawler = VojCrawler()
    main(crawler, OUTPUT_DIR)
