import scrapy
from TextureHavenSpider.items import TexturehavenspiderItem

import os
import re
import logging

class THSpider(scrapy.spiders.Spider):
    name = "TextureHaven"

    allowed_domains = ["texturehaven.com"]

    start_urls = [
        "https://texturehaven.com/textures"
    ]

    main_url = "https://texturehaven.com/"
    main_path = "./Thumbails/"

    # 解析https://texturehaven.com/textures，
    # 获取所有类别的网址、缩略图网址和标签
    def parse(self, response):
        for sel in response.xpath("//div[@class='category-list-images']/ul/a"):
            img_url_text = sel.xpath("li/div/@style").extract()[0]
            categ_url = self.main_url + sel.xpath("@href").extract()[0]
            categ_img = self.main_url + re.search("\/files\/tex\_images\/thumbnails/([\w]*)\.jpg", img_url_text).group()
            categ_tag = sel.xpath("li/p/text()").extract()[0]
            
            yield   scrapy.Request(categ_url, callback=self.categ_parse, 
                meta={"categ_url":categ_url, "categ_img": categ_img, "categ_tag": categ_tag})

    # 解析一类纹理内所有纹理的网址、缩略图网址、标签、
    def categ_parse(self, response):
        for sel in response.xpath("//div[@id='item-grid']/a"):
            textu_url = self.main_url + sel.xpath("@href").extract()[0]
            textu_img = self.main_url +sel.xpath("div/div/img[@class='thumbnail']/@data-src").extract()[0]
            textu_tag = sel.xpath("div/div[@class='description-wrapper']/div/div/h3/text()").extract()[0]

            yield scrapy.Request(textu_url, callback=self.texture_parse,
                meta = {"categ_url":response.meta["categ_url"], 
                        "categ_img": response.meta["categ_img"], 
                        "categ_tag": response.meta["categ_tag"],
                        "textu_url": textu_url, 
                        "textu_img": textu_img, 
                        "textu_tag": textu_tag})
        

    # 解析纹理的下载链接
    def texture_parse(self, response):
        th_item = TexturehavenspiderItem()

        textu_1k = ""
        textu_2k = ""
        textu_4k = ""
        textu_8k = ""

        urls = []

        for sel in response.xpath("//div[@class='map-type'][1]/div[3]/div"):
            urls.append(sel.xpath("a[1]/@href").extract()[0])
        
        for u in urls:
            if "1k" in u:
                textu_1k = self.main_url + u
            if "2k" in u:
                textu_2k = self.main_url + u
            if "4k" in u:
                textu_4k = self.main_url + u
            if "8k" in u:
                textu_8k = self.main_url + u

        th_item["main_path"] = self.main_path
        th_item["categ_url"] = response.meta["categ_url"]
        th_item["categ_img"]= response.meta["categ_img"]
        th_item["categ_tag"] = response.meta["categ_tag"]
        th_item["categ_path"] = self.main_path + "categories_thumbails/" + response.meta["categ_tag"] + ".jpg"

        th_item["textu_url"] = response.meta["textu_url"]
        th_item["textu_img"] = response.meta["textu_img"]
        th_item["textu_tag"] = response.meta["textu_tag"]
        th_item["textu_path"] = self.main_path + response.meta["categ_tag"] + "/" + response.meta["textu_tag"] + ".jpg"

        th_item["textu_1k_url"] = textu_1k
        th_item["textu_2k_url"] = textu_2k
        th_item["textu_4k_url"] = textu_4k
        th_item["textu_8k_url"] = textu_8k

        yield th_item
