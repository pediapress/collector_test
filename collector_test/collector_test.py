#!/usr/bin/env python

"""Collector Test

Usage:
  collector_test [options]

Options:
  -h --help                   Show help.
  -f --fetch <n>              Fetch WP Articles (limit to n fetches)
  -n --numprocs <n>           Number of parallel processes to run [default: 1]
  -m --maxbooks <n>           Number of books to upload [default: 1]
"""


import time
import urllib
import logging
import random
import multiprocessing
import itertools

import requests
import docopt
from splinter import Browser


log = logging.getLogger()


def fetch_wp_article_names(n):
    session = requests.Session()
    query = urllib.parse.urlencode(dict(
        action='query',
        list='random',
        rnnamespace='0',
        rnfiltereddir='nonredirects',
        rnlimit=100,
        format='json'
    ))
    url = 'https://en.wikipedia.org/w/api.php?{}'.format(query)
    for _ in range(n):
        resp = session.get(url)
        data = resp.json()
        titles = [item['title'] for item in data['query']['random']]
        with open('articles.txt', 'a') as f:
            for title in titles:
                f.write(title + '\n')


def build_collection(_id=0):
    log.info('start {}'.format(_id))
    with open('articles.txt') as f:
        articles = [line.strip() for line in f.readlines()]
    base_url = 'https://pediapress.com/collector'
    b = Browser()
    b.visit(base_url)
    b.find_by_xpath('//div[@class="cta"]//a[contains(@class, "btn")]')[0].click()
    b.find_by_text('Wikipedia (en)')[0].click()

    num_articles = random.randint(6, 20)
    log.info('building book with {} articles'.format(num_articles))

    def wait(n=1, msg=''):
        log.info('sleeping {}s ({})'.format(n, msg))
        time.sleep(n)

    def get_element(id=None, xpath=None, css=None):
        element = None
        while not element:
            if id is not None:
                element = b.find_by_id(id)
            elif xpath is not None:
                element = b.find_by_xpath(xpath)
            elif css is not None:
                element = b.find_by_css(css)
            if not element:
                wait(0.5, 'element not present')
        if isinstance(element, list):
            element = element[0]
        while not element.visible:
            wait(0.5, 'element invisible')
        return element

    def add_suggested_article():
        try:
            suggestions = b.find_by_xpath('//ul[@class="suggestions"]/li')
            log.info('got {} suggestions'.format(len(suggestions)))
            e = random.choice(suggestions)
            log.info('adding suggestion {}'.format(e.find_by_css('.ng-binding').text))
            e.find_by_css('.btn').click()
        except:
            log.exception('suggestion exploded')
            return 0
        else:
            return 1

    def add_random_article():
        title = random.choice(articles)
        log.info('adding random article "{}"'.format(title))
        search = get_element(id='article_search')
        search.type(title)
        popup = get_element(xpath='//form//ul[contains(@id, "typeahead")]')
        popup.find_by_xpath('.//a').click()
        return 1

    def send_to_pp():
        b.find_by_xpath('//div[contains(@class, "collection-panel")]//div[@class="panel-footer"]//a')[0].click()
        while not b.is_element_present_by_css('div.coverPreviewArea'):
            wait(1, 'pp preview ready')
    n = 0
    while n < num_articles:
        n += add_random_article()
        wait(2, 'article added')
        n += add_suggested_article()
        wait(2, 'suggested added')
    send_to_pp()
    wait(2, 'done')
    b.quit()


def main():
    args = docopt.docopt(__doc__)
    fetch = args.get('--fetch')
    num_procs = int(args.get('--numprocs'))
    max_books = int(args.get('--maxbooks'))
    if fetch:
        fetch_wp_article_names(int(fetch))
    else:
        if num_procs > 1:
            p = multiprocessing.Pool(processes=num_procs)
            while p.imap_unordered(build_collection, range(max_books), chunksize=1):
                pass
            p.join()
        else:
            for _ in range(max_books):
                build_collection()
