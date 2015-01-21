from __future__ import absolute_import
from celery import shared_task

import time, random
from common_controller.analysis.analysis_blog_review import AnalysisBlogReview
from common_controller.analysis.blog_review_link_scrapper import BlogReviewLinkScrapper


# def analysis_product(self, logger, querys):
@shared_task
def analysis_product(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}
    # blog_review_link_scrapper = BlogReviewLinkScrapper()
    # blog_url_list = blog_review_link_scrapper.startScrapping(query_item_list = querys)
    # analysis_blog_review = AnalysisBlogReview(logger)
    # analysis_result_list = analysis_blog_review.startAnalysis(blog_url_list)
    # return 'good'
    # return http_response_by_json(None, {'analysis_result_list':analysis_result_list} )