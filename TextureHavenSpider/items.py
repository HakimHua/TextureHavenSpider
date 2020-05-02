# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TexturehavenspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    main_path = scrapy.Field()
    categ_url = scrapy.Field()   # 纹理所属类别的网址
    categ_img = scrapy.Field()   # 纹理所属类别的缩略图网址
    categ_tag = scrapy.Field()   # 纹理所属类别的标签
    categ_path = scrapy.Field()  # 纹理所属列别的缩略图的本地地址

    textu_url = scrapy.Field()   # 纹理的网址
    textu_img = scrapy.Field()   # 纹理的缩略图网址
    textu_tag = scrapy.Field()   # 纹理标签
    textu_path = scrapy.Field()  # 纹理缩略图的本地地址

    textu_1k_url = scrapy.Field() # 1k纹理的网址
    textu_2k_url = scrapy.Field() # 2k纹理的网址
    textu_4k_url = scrapy.Field() # 4k纹理的网址
    textu_8k_url = scrapy.Field() # 8k为你的网址
    
