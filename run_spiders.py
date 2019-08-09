#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '24560'
__mtime__ = '2018/6/18'
# qq:2456056533

佛祖保佑  永无bug!

"""
from spiders.xila import Xila, xila_spider


def run_spider():
    from scrapy import cmdline
    cmdline.execute('scrapy crawl {}'.format(xila_spider).split())


def run_all():
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.project import get_project_settings
    from spiderIP.spiders.kuaidaili import KuaiSpider
    from spiderIP.spiders.w66ip import W66Spider
    from spiderIP.spiders.w89ip import W89Spider
    from spiderIP.spiders.xici import XiciSpider
    from twisted.internet import reactor
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    runner.crawl(KuaiSpider)
    runner.crawl(W66Spider)
    runner.crawl(W89Spider)
    runner.crawl(XiciSpider)
    runner.crawl(Xila)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def run_dbIPCheck():
    from spiderIP.dbIPCheck import DbIPCheck

    db_ipcheck = DbIPCheck()
    db_ipcheck.del_ip()


if __name__ == '__main__':
    # run_spider()
    run_all()
    # run_dbIPCheck()
