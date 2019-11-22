# --------------------------------------------------------------------------------------
# File: Exercise_12.2.py
# Name: Amie Davis
# Date: 11/13/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 12.2
#
# Purpose:  Ch 12 Review: Build a Web Spider
#
# Websites Utilized: http://www.emoji-cheat-sheet.com
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
#
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
import scrapy
from scrapyspider.items import EmojiSpiderItem


class EmoSpider(scrapy.Spider):
    name = 'emo'

    allowed_domains = ['emoji-cheat-sheet.com']
    start_urls = ['http://www.emoji-cheat-sheet.com/', ]

    def parse(self, response):

        headers = response.xpath('//h2|//h3')
        lists = response.xpath('//ul')
        all_items = []
        for header, list_cont in zip(headers, lists):
            section = header.xpath('text()').extract()[0]
            for li in list_cont.xpath('li'):
                item = EmojiSpiderItem()
                item['section'] = section
                spans = li.xpath('div/span')
                if len(spans):
                    link = spans[0].xpath('@data-src').extract()
                    if link:
                        item['emoji_link'] = response.url + link[0]
                    handle_code = spans[1].xpath('text()').extract()
                else:
                    handle_code = li.xpath('div/text()').extract()
                if handle_code:
                    item['emoji_handle'] = handle_code[0]
                all_items.append(item)
        return all_items