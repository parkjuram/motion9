# -*- coding:utf-8 -*-
import requests
from urllib import quote
from bs4 import BeautifulSoup

class BlogReviewLinkScrapper:
    def __init__(self):
        self.custom_headers = {
            'Host': 'cafeblog.search.naver.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cookie': 'page_uid=S64BBdpySD0ssZK3Qx0ssssssss-132607; _naver_usersession_=VKIjjQpyVl0AAEM3dC4; nx_open_so=1; NNB=YILAICUNEORFI; npic=irlG+thL73mVV+IJbIBdWkKD0H2abnmwTxh/9pPkmeu+rvV74vf7rxJeOcu7Z2v8CA=='
        }

        self.query_start_url = "http://cafeblog.search.naver.com/search.naver?sm=tab_hty.top&where=post&ie=utf8&query="
        self.query_end_url = "&st=sim&date_option=0&date_from=&date_to=&dup_remove=1&post_blogurl=&post_blogurl_without=&srchby=all&nso=&ie=utf8&start="

    def startScrapping(self, query_item_list):
        self.blog_url_list = []

        for query_item_url in query_item_list:
            query_item_url = quote(query_item_url)

            for start in range(1,1000,10):
                if start == 1:
                    full_url = self.query_start_url + query_item_url
                else:
                    full_url = self.query_start_url + query_item_url + self.query_end_url + str(start)

                r = requests.request(method='GET', url=full_url, headers=self.custom_headers )
                soup = BeautifulSoup(r.text)
                r.close()
                blog_list = soup.select('.sh_blog_top')

                for blog_item in blog_list:
                    if not(blog_item.select('._sp_each_url')[0]['href'] in self.blog_url_list):
                        self.blog_url_list.append(blog_item.select('._sp_each_url')[0]['href'])

                if len(blog_list) != 10:
                    break

        return self.blog_url_list
