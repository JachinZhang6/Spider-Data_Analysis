#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
__author__ = 'Jachin'
from selenium import webdriver
from retrying import retry
import time
import json


class DouYu():
    def __init__(self):
        self.start_url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome()

    @retry(stop_max_attempt_number=5)  # 尝试多次请求
    def get_content_list(self):
        li_list = self.driver.find_elements_by_xpath("//ul[@class='layout-Cover-list']/li")
        content_list = []
        for li in li_list:
            item = {}
            item["img"] = li.find_element_by_xpath(".//img[@class='DyImg-content is-normal ']").get_attribute('src')
            item['url'] = li.find_element_by_xpath(".//a[@class='DyListCover-wrap']").get_attribute('href')
            item['title'] = li.find_element_by_xpath(".//h3[@class='DyListCover-intro']").get_attribute('title')
            item['categroies'] = li.find_element_by_xpath(".//span[@class='DyListCover-zone']").text
            item['watch_num'] = li.find_element_by_xpath(".//span[@class='DyListCover-hot']").text
            item['anchor'] = li.find_element_by_xpath(".//h2[@class='DyListCover-user']").text
            print(item)
            content_list.append(item)

        # 提取下一页元素
        next_url = self.driver.find_elements_by_xpath("//span[@class='dy-Pagination-item-custom']")
        next_url = next_url[0] if len(next_url) > 0 else None

        return content_list, next_url

    def save_content_list(self, content_list):
        with open('douyu2.txt', 'a', encoding='utf-8')as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print("已保存成功")

    def run(self):
        # 1. 准备url
        # 2. 发送请求,获取响应
        self.driver.get(self.start_url)
        # 3. 提取数据,提取下一页的元素
        content_list, next_url = self.get_content_list()
        # 4. 保存
        self.save_content_list(content_list)
        # 5. 点击下一页，数据的提取循环
        while next_url is not None:
            next_url.click()  # 页面没有完全加载完,会报错
            time.sleep(2)
            content_list, next_url = self.get_content_list()
            self.save_content_list(content_list)


if __name__ == '__main__':
    douyu = DouYu()
    douyu.run()
