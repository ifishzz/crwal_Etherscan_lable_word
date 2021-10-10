# -*- coding: utf-8 -*-
"""
Created on 2021-10-09 14:04:51
---------
@summary:
---------
@author: ifish
"""

import feapder
from bs4 import BeautifulSoup
import urllib


class FirstSpider(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("https://etherscan.io/labelcloud")

    def download_midware(self, request):
        request.cookies = {
            "ASP.NET_SessionId": "one0xx0ls0uqr5q0zwzd2wym",
            "__cflb": "02DiuFnsSsHWYH8WqVXbZzkeTrZ6gtmGVjv82GaDCEcvY",
            "_ga": "GA1.2.1440548348.1633759767",
            "_gid": "GA1.2.142127217.1633759767",
            "__cf_bm": "YNfNxJTe9X8K1Z2dHy0FzBdC45FNAkuK3MaokcgKpag-1633771551-0-AbukH13SR//n+94/qxBFoI6fcB+ZnVxS0yCApUOeXMVJkdzIVqMOzOtutGFdH0GEz5ztqkHftZO5pcGD6O7VSOkKssm5WZCKmr4q4LPGJ62+17hpbM7ulpya5Qbf62Jd6+96AWSCXDH4/K+2kEiD5DA=",
            "etherscan_userid": "0x007er",
            "etherscan_pwd": "4792:Qdxb:QcfcMJ8HXkw2J5Ce4pDXi1A2pHcTvP8qQW6Zi9jWgbA=",
            "etherscan_autologin": "True",
            "_gat_gtag_UA_46998878_6": "1"
        }

        return request

    def parse(self, request, response):
        article_list = response.xpath('//a[@class="py-1 px-3 d-block"]')
        for article in article_list:
            title = article.xpath("./text()").extract_first()
            url = article.xpath("./@href").extract_first()
            coin_name = url.rsplit('/', 1)[-1]
            if 'accounts' in url:
                url = f"{url}?subcatid=undefined&size=1000&start=0&col=1&order=asc"

                yield feapder.Request(
                    url, callback=self.parse_detail, title=title, coin_name=coin_name)  # callback 为回调函数

    def parse_detail(self, request, response):
        """
        解析详情
        """
        # 取title
        # title = request.title
        url = request.url
        coin_name = request.coin_name

        print("url", url)
        print("coin_name", coin_name)
        # print("title", title)

        # Address = response.xpath(
        #     '//i[@class="far fa-file-alt text-secondary mr-1"]/following-sibling::a[1]/text()').extract()
        # name_tag = response.xpath(
        #     '//i[@class="far fa-file-alt text-secondary mr-1"]/../../following-sibling::td[1]/text()').extract()

        # print(Address)
        # print(name_tag)
        adds = response.xpath(
            '//tbody/tr/td/a/text() | //tbody/tr/td/span/a/text()').getall()
        tags = response.xpath('//tbody/tr/td[2]/text()').getall()
        print(adds)
        print(tags)

        for i in range(0, len(adds)):
            print(f"add:{adds[i]} tag:{tags[i] if tags else ''}")
    # address = response.xpath(
    #     '//tbody/tr/td/a/text()').extract()
    # # print(address)
    # name_tag = response.xpath(
    #     '//tbody/tr/td/a/../../following-sibling::td[1]/text()').extract()
    # # print(name_tag)

    #
    # address_contract = response.xpath(
    #     '//tbody/tr/td/span/a/text()').extract()
    # print(address_contract)
    #
    # name_tag_contract = response.xpath(
    #     '//tbody/tr/td/span/a/../../following-sibling::td[1]/text()').extract()
    # print(name_tag_contract)
    #
    # res1 = dict(zip(address, name_tag))
    # res2 = dict(zip(address_contract, name_tag_contract))
    # print(res1)
    # print(res2)

    # soup = BeautifulSoup(response.text, 'html.parser')
    # tbodys = soup.find_all('tbody')
    # for tbody in tbodys:
    #     trs = tbody.find_all('tr')
    #     for tr in trs:
    #         tds = tr.find_all('td')
    #         address = tds[0].get_text()
    #         tagname = tds[1].get_text()
    #         print("Address: " + address + ", Name Tag: " + tagname)
    #         try:
    #             with open('test111.txt', 'a+', encoding='utf-8') as f:
    #                 f.write(
    #                     f"INSERT INTO `label`(`address`,`tag`, `label`,) VALUES ('{address}','{tagname}', '{coin_name}');\n")
    #         except Exception as e:
    #             print(e)


if __name__ == "__main__":
    FirstSpider().start()
