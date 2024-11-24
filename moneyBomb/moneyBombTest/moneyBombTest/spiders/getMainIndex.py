import json
import pandas as pd
import scrapy


class GetstockcodeSpider(scrapy.Spider):
    print("爬取股票指数")
    name = "getMainIndex"
    # allowed_domains = ["quote.eastmoney.com"]
    start_urls = ["https://push2.eastmoney.com/api/qt/ulist.np/get?ut=6d2ffaa6a585d612eda28417681d58fb&fields=f1,f2,"
                  "f3,f12,f13,f4,f14&secids=1.000001,0.399001,0.399006,1.000300,0.399005,1.000016,1.000688,1.000003"]

    def parse(self, response):
        # 假设response.text是从网络获取的JSON字符串
        jsonp_data = response.text
        print(jsonp_data)

        # 去掉前后的非JSON部分，确保获取纯JSON格式的字符串
        json_str = jsonp_data[jsonp_data.index('{'):jsonp_data.rindex('}') + 1]

        # 解析JSON数据
        data = json.loads(json_str)

        # 提取和处理股票指数数据
        diff = data['data']['diff']
        indices_data = [{
            'symbol': item['f12'],
            'name': item['f14'],
            'index_value': item['f2'] / 100,
            'change_percent': item['f3'] / 100,
            'change_amount': item['f4'] / 100,
        } for item in diff]

        # 创建DataFrame
        df = pd.DataFrame(indices_data)

        # 保存到CSV文件
        df.to_csv('data/stock_indices.csv', index=False, encoding='utf-8-sig')
