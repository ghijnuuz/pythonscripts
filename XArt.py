#!/usr/bin/python

import sys
import os
import logging
import re
from datetime import datetime
from bs4 import BeautifulSoup
try:    # Python 3
	import urllib.parse as urllib
except: # Python 2
	import urllib as urllib

# Video Info dict
# {
#     'URL'       :'url',
#     'Title'     :'title',
#     'Date'      :date,
#     'Models'    :['model1','model2'],
#     'Rating'    :9.9,
#     'VoteCount' :100
# }

class XArt:
    root_xart_url = 'http://x-art.com/'
    root_video_url = 'http://x-art.com/videos/'

    def __init__(self):
        self.is_last_page = False
        self.next_page_url = XArt.root_video_url

    def get_video_info_list(self):
        video_info_list = []
        vl = self.get_video_url_list()
        for video_url in vl:
            video_info_list.append(self.get_video_info(video_url))
        return video_info_list

    def get_video_info(self, video_url):
        html_doc = ''
        video_info = {}
        try:
            logging.info(video_url)
            html_doc = urllib.urlopen(video_url).read()
        except:
            logging.error('Unable to connect to server.Please try again after using a proxy.')
        video_info = self.parser_video_info_html(html_doc)
        video_info['URL'] = video_url
        return video_info

    def parser_video_info_html(self, html_doc):
        video_info = {}
        soup = BeautifulSoup(html_doc)

        # Get Title
        data = soup.select('#content > h1')
        if len(data) > 0:
            video_info['Title'] = unicode(data[0].contents[0])

        # Get Date
        data = soup.select('#content > .head-list > li')
        if len(data) == 2:
            date_str = str(unicode(data[0].contents[1])).strip()
            video_info['Date'] = datetime.strptime(date_str,  '%b %d, %Y').date()

        # Get Models
        data = soup.select('#content > .head-list > li > a')
        if len(data):
            video_info['Models'] = []
            for model in data:
                video_info['Models'].append(unicode(model.contents[0]))

        # Get Rating and VoteCount
        data = soup.select('.star-holder > p')
        if len(data):
            votes_list = data[0].contents[0]
            votes_list = re.split('/| |\(|\)', votes_list)
            votes_list.remove('')
            video_info['Rating'] = float(unicode(votes_list[0]))
            video_info['VoteCount'] = int(unicode(votes_list[2]))

        return video_info

    def get_video_url_list(self):
        logging.info('Start get video list.')
        self.is_last_page = False
        html_doc = ''
        video_url_list = []
        while self.is_last_page == False:
            try:
                logging.info(self.next_page_url)
                html_doc = urllib.urlopen(self.next_page_url).read()
            except:
                logging.error('Unable to connect to server.Please try again after using a proxy.')
            video_url_list += self.parser_video_url_list_html(html_doc)
        logging.info('Total ' + str(len(video_url_list)) + ' video url.')
        return video_url_list

    def parser_video_url_list_html(self, html_doc):
        video_list = []
        soup = BeautifulSoup(html_doc)

        data = soup.select('a.image')
        for image in data:
            video_list.append(str(image.attrs['href']))

        logging.info('Get %d video url.' % (len(video_list)))

        data = soup.select('.right_links > a')
        if len(data) > 0 and data[0].attrs['href'] != 'javascript:void(0)':
            self.next_page_url = XArt.root_xart_url + data[0].attrs['href']
            self.is_last_page = False
        else:
            self.next_page_url = XArt.root_video_url
            self.is_last_page = True
            logging.info('Last video list page.')

        return video_list

    def convert_to_custom_str_list(self, video_info_list):
        custom_str_list = []
        for video_info in video_info_list:
            custom_str_list.append(self.convert_to_custom_str(video_info))
        return custom_str_list

    def convert_to_custom_str(self, video_info):
        models_str = ' & '.join(video_info['Models'])
        custom_str = 'X-Art %s %s - %s' \
                     % (video_info['Date'].strftime('%Y%m%d'), models_str, str(video_info['Title']))
        return custom_str

def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a+')

    x = XArt()
    video_info_list = x.get_video_info_list()
    custom_str_list = x.convert_to_custom_str_list(video_info_list)

    f = file('XArtVideoName.txt', 'w')
    for name_str in custom_str_list:
        f.write(name_str + u'\r\n')
    f.close()

    logging.info('Finish write file.')

if __name__ == '__main__':
    main()