# -*- coding: utf-8 -*-
import scrapy
import urlparse,urllib,traceback,sys
from ilovemid.items import IlovemidItem
from scrapy import log,Request
from HTMLParser import HTMLParser

class IlovemidBotSpider(scrapy.Spider):
    name = "ilovemid_bot"
    allowed_domains = ["ilovemid.cafe24.com"]
    start_urls = (
        'http://ilovemid.cafe24.com/bbs/group.php?gr_id=USA_end',
    )
    tumbnails = {}

    def __init__(self, *args, **kwargs):
        super(IlovemidBotSpider, self).__init__(*args, **kwargs)
        self.group_chain = []
        self.show_chain = []
        self.episode_chain = []
    def start_requests(self):
        return [scrapy.FormRequest("http://ilovemid.cafe24.com/bbs/board.php?bo_table=Lost",
                                   callback=self.parse_show)]

    def compare(self,item1, item2):
        id1 = item1[0]
        id2 = item2[0]
        print('id1 = %s id2=%s'%(item1,item2))
        return int(id1) - int(id2)
    def parse(self, response):
        try:
            selector = scrapy.Selector(response)
            # At first: getting items to be parsed

            show_links = selector.css('strong[class=lt_title] a::attr(href)').extract()
            count = len(show_links)
            log.msg('*********Reached parse Shows , %s'%count, level=log.DEBUG)

            for show_link in show_links:
                self.show_chain.append(
                    scrapy.http.Request(show_link, callback=self.parse_show))
            if self.show_chain:
                yield self.show_chain.pop(0)
                # return self.group_chain
        except:
            traceback.print_exc(file=sys.stdout)


    def parse_show(self,response):
        selector = scrapy.Selector(response)
        episode_links = selector.css('td[class=list-subject] a::attr(href)').extract()
        # episode_links = sorted(episode_links,cmp=self.compare)
        count = len(episode_links)
        log.msg('*********Reached parse Episodes , %s'%count, level=log.DEBUG)
        tbl =  selector.css('table[class=list-tbl]')
        tpls = ()
        if '&page=' not in response.url:
            pagination = set(selector.css(".paginate a::attr('href')").extract())
            log.msg('Pagination-->%s'%pagination,level=log.DEBUG)
            for link in pagination:
                self.show_chain.insert(0,
                        scrapy.http.Request(link, callback=self.parse_show))

        for lst in tbl.xpath(".//tr"):
            url = lst.xpath(".//td[@class='list-subject']/a/@href").extract()
            listnum = lst.xpath(".//td[@class='list-num']/text()").extract()
            if len(url) > 0 and len(listnum) > 0 :
                tpls += ((listnum[0],url[0]),)
        # print tpls
        sorted(tpls,key=lambda item: item[0])
        for num,episode_link in tpls:
            self.show_chain.append(
                    scrapy.http.Request(episode_link, callback=self.parse_episode))



        if self.show_chain:
            yield self.show_chain.pop(0)
        #     return self.episode_chain


    def parse_episode(self,response):
        log.msg('Inside parse_episode ********************',log.DEBUG)
        selector = scrapy.Selector(response)
        item = IlovemidItem()
        item['url'] = response.url
        image_ele =  selector.xpath("//div[@id='main_content']/div/img/@src")
        log.msg(image_ele,log.DEBUG)
        if len(image_ele) > 0:
            item['image_url'] = image_ele.extract()
        else :
            image_ele = selector.xpath("//article[@id='bo_v_atc']/div/div/div")
            if len(image_ele) > 0:
                item['image_url'] = image_ele[0].xpath('.//img/@src').extract()
            else :
                image_ele = selector.xpath("//article[@id='bo_v_atc']/div")
                if len(image_ele) > 0:
                    item['image_url'] = image_ele[0].xpath('.//img/@src').extract()
        title =  response.xpath("//div[@class='view_head']/*/header/h1/text()").extract()
        item['title'] = title
        for_pub_date = response.xpath("//section[@id='bo_v_info']/ul/li[@class='last']/span/text()").extract()
        item['posted_date_time'] = for_pub_date
        # if len(response.xpath("//section[@id='bo_v_info']/ul/li")) > 1 :
        #     tags = response.xpath("//section[@id='bo_v_info']/ul/li")[1].xpath('.//text()').extract()
        #     item['tags'] = tags
        tag_elem = response.xpath("//article[@id='bo_v_atc']/div[@class='view_tag']/text()")
        if len(tag_elem) > 0:
            item['tags'] = response.xpath("//article[@id='bo_v_atc']/div[@class='view_tag']/text()").extract()[0]
        else:
            tag_elem = response.xpath("//div[@id='bo_v']/div[@class='view_head']/div[@class='subject']/header/h1/text()").extract()
            if len(tag_elem) > 0:
                item['tags'] = tag_elem[0]

        embed_urls_root = response.xpath("//article[@id='bo_v_atc']/div[@class='viewContents']")
        embed_urls = embed_urls_root.xpath(".//a/@href").extract()
        if len(embed_urls) == 0:
            embed_urls = selector.css(".m_video-container iframe::attr(src)").extract()

        decription_ele = response.xpath("//article[@id='bo_v_atc']/div/div/span/span/span/text()").extract()
        if len(decription_ele) > 0:
            item['description'] = decription_ele[0]
        cat_string = response.xpath("//span[@class='on old']/text()").extract()
        if len(cat_string) > 0:
            i = cat_string[0].index('(')
            item['category'] = cat_string[0][0:i]
        season_ele  = response.xpath("//section[@id='bo_v_info']/ul/li[position()=2]/text()").extract()
        if len(season_ele) > 0 :
            item['season'] = season_ele[0]
        def update_url(url):
            u = urllib.unquote(h.unescape(url))
            log.msg('Inside parse_episode ********************URL-->%s'%u,log.DEBUG)
            return u.encode('utf-8');
            # splitted = urlparse.urlsplit(url)
            # print url
            # print splitted
            # return ''.join(
            #     [
            #         splitted.scheme or 'http',
            #         '://',
            #         splitted.netloc,
            #         urllib.quote(splitted.path),
            #         '?' if splitted.query else '',
            #         urllib.quote(splitted.query),
            #         '#' if splitted.fragment else '',
            #         urllib.quote(splitted.fragment)
            #     ]
            # )
        h = HTMLParser()
        item['embed_urls'] = [
            {'embed': {
                'src': url,
                'width': "480",
                'height': "400"}
            } for url in embed_urls[:2]]

        yield item
        if self.show_chain:
            yield self.show_chain.pop(0)
