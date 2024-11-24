import csv
import json
import pandas as pd
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
import subprocess
import os

import scrapy


# from moneyBombTest.items import MoneybombtestItem

class MoneySpider(scrapy.Spider):
    name = "getSingleStockData"
    allowed_domains = ["emweb.securities.eastmoney.com"]
    start_urls = ["https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/PageAjax?code=SZ300059"]

    # def saveToMysql(self):
    #     # 当爬虫关闭时，执行csv2mysql.py
    #     subprocess.call(['python', 'csv2mysql.py'])

    def parse(self, response):
        info = json.loads(response.text)  # 得到json并解析

        zyfw = pd.json_normalize(info['zyfw'])
        zygcfx = pd.json_normalize(info['zygcfx'])
        jyps = pd.json_normalize(info['jyps'])

        # 修改字段名
        jyps.rename(columns={"SECUCODE": "stock_code_with_exchange",
                             "SECURITY_CODE": "stock_code",
                             "REPORT_DATE":"report_date",
                             "BUSINESS_REVIEW":"business_review"}, inplace=True)
        zyfw.rename(columns={"SECUCODE":"stock_code_with_exchange",
                             "SECURITY_CODE": "stock_code",
                             "BUSINESS_SCOPE":"business_scope"}, inplace=True)
        zygcfx.rename(columns={"SECUCODE":"stock_code_with_exchange",
                               "SECURITY_CODE": "stock_code",
                               "REPORT_DATE":"report_date",
                               "MAINOP_TYPE":"mainop_type",
                               "ITEM_NAME":"item_name",
                               "MAIN_BUSINESS_INCOME":"main_business_income",
                               "MBI_RATIO":"mbi_ratio",
                               "RANK":"rank",
                               "MAIN_BUSINESS_COST":"main_business_cost",
                               "MBC_RATIO":"mbc_ratio",
                               "MAIN_BUSINESS_RPOFIT":"main_business_profit",
                               "MBR_RATIO":"mbr_ratio",
                               "GROSS_RPOFIT_RATIO":"gross_profit_ratio"}, inplace=True,
                        )
#SECUCODE,SECURITY_CODE,REPORT_DATE,MAINOP_TYPE,ITEM_NAME,MAIN_BUSINESS_INCOME,MBI_RATIO,RANK,MAIN_BUSINESS_COST,MBC_RATIO,MAIN_BUSINESS_RPOFIT,MBR_RATIO,GROSS_RPOFIT_RATIO
        zyfw.to_csv("data/primary_business_field.csv", index=None)
        zygcfx.to_csv("data/primary_business_component_analysis.csv", index=None)
        jyps.to_csv("data/business_review.csv", index=None)
        # self.saveToMysql()
