import scrapy
import json
import pandas as pd


class MoneySpider(scrapy.Spider):
    print("爬取predict")
    name = "getPredict"
    start_urls = [
        "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=datatable4712512&reportName=RPT_WEB_RESPREDICT&columns=WEB_RESPREDICT&pageNumber={}&pageSize=500&sortTypes=-1&sortColumns=RATING_ORG_NUM".format(
            i) for i in range(1, 7)
    ]

    def __init__(self, *args, **kwargs):
        super(MoneySpider, self).__init__(*args, **kwargs)
        self.data_frame = pd.DataFrame()  # 初始化空的DataFrame

    def parse(self, response):
        # 去掉前后的非JSON部分
        json_str = response.text[response.text.index('{'):response.text.rindex('}') + 1]

        # 解析JSON数据
        data = json.loads(json_str)

        # 提取需要的字段
        data_list = data['result']['data']
        filtered_data = [{
            'stock_code': item.get('SECURITY_CODE'),
            'RATING_ORG_NUM': item.get('RATING_ORG_NUM'),
            'RATING_BUY_NUM': item.get('RATING_BUY_NUM'),
            'RATING_ADD_NUM': item.get('RATING_ADD_NUM'),
            'RATING_NEUTRAL_NUM': item.get('RATING_NEUTRAL_NUM'),
            'RATING_REDUCE_NUM': item.get('RATING_REDUCE_NUM'),
            'RATING_SALE_NUM': item.get('RATING_SALE_NUM'),
            'YEAR1': item.get('YEAR1'),
            'EPS1': item.get('EPS1'),
            'YEAR2': item.get('YEAR2'),
            'EPS2': item.get('EPS2'),
            'YEAR3': item.get('YEAR3'),
            'EPS3': item.get('EPS3'),
            'YEAR4': item.get('YEAR4'),
            'EPS4': item.get('EPS4'),
        } for item in data_list]

        # 创建DataFrame并将数据添加到爬虫的DataFrame中
        new_data = pd.DataFrame(filtered_data)
        self.data_frame = pd.concat([self.data_frame, new_data], ignore_index=True)
        self.data_frame.to_csv('data/predict.csv', index=False, encoding='utf-8-sig')
