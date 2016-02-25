# -*- coding: utf-8 -*-

import scrapy
from zhejiang.items import ZhejiangItem


class ZheJiang(scrapy.Spider):
    name = 'zhejiang'
    allowed_domains = ['china.findlaw.cn']
    start_urls = [
        'http://china.findlaw.cn/zhejiang/sifaju/orglist_1',
        'http://china.findlaw.cn/zhejiang/jianchayuan/orglist_1',
        'http://china.findlaw.cn/zhejiang/gonganju/orglist_1']

    def parse(self, response):
        block = response.css('.conts.bt1 .inlawerlist')
        for info in block:
            item = ZhejiangItem()
            item['name'] = info.css('dd .name a::text').extract()
            item['address'] = info.css('dd .other:nth-child(even)::text').extract()
            item['tel'] = info.css('dt span::text').extract()
            yield item

        next_page = response.css('.page a::attr(href)').extract()[-1]
        if next_page != '#':
            link = response.urljoin(next_page)
            yield scrapy.Request(link, self.parse)
