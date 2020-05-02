# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

import os
import sqlite3


class SQLitePipeline(object):
    def open_spider(self, spider):
        self.conn = sqlite3.connect("./Thumbails/TextureHavenDataSet.db")
        sql_cmd = "CREATE TABLE IF NOT EXISTS TEXTUREHAVEN \
            (                                              \
                textu_tag  TEXT  PRIMARY KEY,              \
                categ_tag  TEXT,                           \
                textu_img  TEXT,                           \
                categ_img  TEXT,                           \
                textu_path TEXT,                           \
                categ_path TEXT,                           \
                textu_1k_url  TEXT,                        \
                textu_2k_url TEXT,                         \
                textu_4k_url  TEXT,                        \
                textu_8k_url  TEXT                        \
            )"
    
        self.conn.execute(sql_cmd)
        self.conn.commit()
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()
        
    def process_item(self, item, spider):
        sql_cmd = "INSERT INTO TEXTUREHAVEN               \
            (textu_tag, categ_tag, textu_img, categ_img,   \
            textu_path, categ_path, textu_1k_url, textu_2k_url, \
            textu_4k_url, textu_8k_url)                  \
            VALUES        \
            (                                             \
            :textu_tag, :categ_tag, :textu_img, :categ_img,   \
            :textu_path, :categ_path, :textu_1k_url, :textu_2k_url, \
            :textu_4k_url, :textu_8k_url    \
            )"
        self.cur.execute(sql_cmd, {
            "textu_tag": item["textu_tag"],
            "categ_tag": item["categ_tag"],
            "textu_img": item["textu_img"],
            "categ_img": item["categ_img"],
            "textu_path": item["textu_path"],
            "categ_path": item["categ_path"],
            "textu_1k_url": item["textu_1k_url"],
            "textu_2k_url": item["textu_2k_url"],
            "textu_4k_url": item["textu_4k_url"],
            "textu_8k_url": item["textu_8k_url"],
        })
        self.conn.commit()

class TexturehavenspiderPipeline:
    def process_item(self, item, spider):
        if not os.path.exists(item["main_path"]):
            os.mkdir(item["main_path"])
        
        if not os.path.exists(item["main_path"] + "categories_thumbails/"):
            os.mkdir(item["main_path"] + "categories_thumbails/")

        if not os.path.exists(item["main_path"] + item["categ_tag"]):
             os.mkdir(item["main_path"] + item["categ_tag"])
        return item


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        categ_img_url = item["categ_img"]
        yield scrapy.Request(categ_img_url, meta={"path": item["categ_path"]})

        textu_img_url = item["textu_img"]
        yield scrapy.Request(textu_img_url, meta={"path": item["textu_path"]})

    def item_completed(self, results, item, info):
        if not results[0][0]:
            with open('img_error.txt', 'a')as f:
                error = str(item['categ_path']+' '+item['categ_img'])
                f.write(error)
                f.write('\n')
                raise DropItem("Failed to download!")
        return item
    
    def file_path(self, request, response=None, info=None):
        name = request.meta['path']

        return name