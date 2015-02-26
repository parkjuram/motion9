# -*- coding:utf-8 -*-
from __future__ import absolute_import
from celery import shared_task, task

from celery.utils.log import get_task_logger
from common_controller.analysis.analysis_blog_review import AnalysisBlogReview
from common_controller.analysis.blog_review_link_scrapper import BlogReviewLinkScrapper

logger = get_task_logger(__name__)

# def analysis_product(self, logger, querys):
@task(bind=True)
def analysis_product(self, querys):
    blog_review_link_scrapper = BlogReviewLinkScrapper(logger)

    logger.info(querys)

    blog_url_list = blog_review_link_scrapper.startScrapping(query_item_list = querys)

    logger.info( blog_url_list )

    analysis_blog_review = AnalysisBlogReview()
    analysis_result = analysis_blog_review.startAnalysis( self, blog_url_list)


    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': analysis_result}
    # return http_response_by_json(None, {'analysis_result_list':analysis_result_list} )