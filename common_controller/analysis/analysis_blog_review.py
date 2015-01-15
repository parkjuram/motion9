# -*- coding:utf-8 -*-
import operator
import jpype
from konlpy.tag import Hannanum
import requests
from urllib import quote
from bs4 import BeautifulSoup

class AnalysisBlogReview:

    def __init__(self, logger):
        self.logger = logger
        self.analysis_result = {}
        self.skip_count=0

    def startAnalysis(self, blog_url_list):
        self.analysis_result = {}
        self.skip_count=0
        for blog_review_url in blog_url_list:
            self.analysis(blog_review_url)

        sorted_analysis_result = sorted(self.analysis_result.items(), key=operator.itemgetter(1), reverse=True)
        analysis_result_list = []

        for item in sorted_analysis_result:
            analysis_result_list.append({'keyword':item[0], 'count':item[1]})

        return analysis_result_list

    def analysis(self, blog_review_url):
        self.logger.info(blog_review_url)

        analysis_checker = {}

        r = requests.get(quote(blog_review_url))
        soup = BeautifulSoup(r.text)
        r.close()

        try:
            blog_review_url = soup.select('#screenFrame')[0]['src']
            r = requests.get(blog_review_url)
            soup = BeautifulSoup(r.text)
            r.close()
        except Exception as e:
            pass

        try:
            real_blog_review_url = "http://blog.naver.com" + soup.select('frame#mainFrame')[0]['src']
        except IndexError as e:
            self.skip_count+=1
            return

        r = requests.get(real_blog_review_url)
        soup = BeautifulSoup(r.text)
        r.close()

        post_view = soup.select('.post-view')[0]
        p_list = post_view.select('p')

        raw_str_list = []
        for item in p_list:
            p_str = str(item.text.encode('utf-8')).replace('\xc2\xa0',' ').replace('\xe2\x80\x8b',' ').strip()
            p_str = p_str.replace('ㅎ','').replace('ㅋ','')
            if len(p_str)!=0:
                raw_str_list.append(p_str.decode('utf-8'))

        kkma = Hannanum()

        for raw_str_item in raw_str_list:
            if len(raw_str_item) >= 100:
                self.skip_count+=1
                continue

            try:
                raw_str_item = raw_str_item.strip()
                pos_tuple = kkma.pos(raw_str_item)
                for pos_tuple_item in pos_tuple:
                    item = pos_tuple_item[0]
                    item_type = pos_tuple_item[1]

                    if not(analysis_checker.has_key(item)) and (item_type.startswith('N') or item_type.startswith('V') or item_type.startswith('M') or item_type.startswith('XR') or item_type.startswith('U')):
                        if self.analysis_result.has_key(item):
                            analysis_item_count = self.analysis_result.get(item) + 1
                        else:
                            analysis_item_count = 1

                        self.analysis_result.update({
                                               item: analysis_item_count
                                               })

                        analysis_checker.update({
                            item:1
                        })
            except jpype.JavaException as exception:
                self.logger.info("java exception!")
                # print exception.message()
                # print exception.stacktrace()
