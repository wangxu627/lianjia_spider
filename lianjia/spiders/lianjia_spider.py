import scrapy
import re
from urls import urls
from lianjia.items import LianjiaItem

class LianjiaSpiderSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["cd.lianjia.com"]
    # start_urls = ["https://cd.lianjia.com"]
    # start_urls = ['https://cd.lianjia.com/ershoufang/chuanshi/pg1']
    start_urls = urls
    # def start_requests(self):
    #     start_urls = [url1, url2, url3]  # 从任何来源获取您的动态URL列表
    #     for url in start_urls:
    #         yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 解析<ul class="sellListContent">中的<li>元素
        house_list = response.css('ul.sellListContent li')
        
        for house in house_list:
            # 提取data-lj-view_evtid中的值
            lj_action_resblock_id = house.attrib.get("data-lj_action_resblock_id") 
            lj_action_housedel_id = house.attrib.get("data-lj_action_housedel_id")
            detail_url = house.css('a::attr(href)').get()
            title = house.css('div.info div.title a::text').get()
            good_house_tag = house.css("div.info div.title span.goodhouse_tag").get() is not None
            block = house.css("div.info div.flood div.positionInfo a:nth-of-type(1)::text").get()
            region = house.css("div.info div.flood div.positionInfo a:nth-of-type(2)::text").get()
            address_info = house.css("div.info div.address div.houseInfo::text").get()
            layout, area, orientation, renovation, floor, year, build_type = self.get_address_detail(address_info)
            total_price = house.css('div.info div.priceInfo div.totalPrice *::text').getall()
            unit_price = house.css('div.info div.priceInfo div.unitPrice *::text').getall()
            follow_info = house.css('div.info div.followInfo::text').get()
            star_count, release_date = [info.strip() for info in follow_info.split("/")]

            # yield {
            #     'lj_action_resblock_id': lj_action_resblock_id,
            #     "lj_action_housedel_id": lj_action_housedel_id,
            #     "detail_url": detail_url,
            #     "title": title,
            #     "total_price": "".join(total_price).strip(),
            #     "unit_price": "".join(unit_price).strip(),
            #     "good_house_tag": good_house_tag,
            #     "block": block,
            #     "region": region,
            #     "layout": layout,
            #     "area": area,
            #     "orientation": orientation,
            #     "renovation": renovation,
            #     "floor": floor,
            #     "year": year,
            #     "build_type": build_type,
            #     "star_count": star_count,
            #     "release_date": release_date
            # }
            item = LianjiaItem(
                lj_action_resblock_id = lj_action_resblock_id,
                lj_action_housedel_id = lj_action_housedel_id,
                detail_url = detail_url,
                title = title,
                total_price = "".join(total_price).strip(),
                unit_price = "".join(unit_price).strip(),
                good_house_tag = good_house_tag,
                block = block,
                region = region,
                layout = layout,
                area = area,
                orientation = orientation,
                renovation = renovation,
                floor = floor,
                year = year,
                build_type = build_type,
                star_count = star_count,
                release_date = release_date
            )
            yield item

        if len(house_list) > 0:
            match = re.search(r'/pg(\d+)', response.url)
            if match:
                page_number = int(match.group(1)) + 1
                new_url = re.sub(r'/pg\d+', f'/pg{page_number}', response.url)
                yield response.follow(new_url, callback=self.parse)


    def get_address_detail(self, address_info):
        address_info_list = [address.strip() for address in address_info.split("|")]
        if len(address_info_list) == 7:
            layout, area, orientation, renovation, floor, year, build_type = address_info_list
        elif len(address_info_list) == 6:
            layout, area, orientation, renovation, floor, build_type = address_info_list
            year = 0
        else:
            layout, area, orientation, renovation, floor, year, build_type = ["", "", "", "", "", "", ""]
        return layout, area, orientation, renovation, floor, year, build_type