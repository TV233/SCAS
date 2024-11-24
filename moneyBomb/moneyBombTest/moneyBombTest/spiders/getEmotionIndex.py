import json
import pandas as pd
import scrapy


class GetstockcodeSpider(scrapy.Spider):
    print("爬取市场情绪指数emotion_index")
    name = "getEmotionIndex"
    # allowed_domains = ["quote.eastmoney.com"]
    start_urls = ["https://quote.eastmoney.com/ztb/api/gbtrend?type=3"]

    def parse(self, response):
        # print(response.text)
        jsonp_data = response.text
        print(jsonp_data)
        # 去掉前后的非JSON部分
        json_str = jsonp_data[jsonp_data.index('{'):jsonp_data.rindex('}') + 1]

        # 解析JSON数据
        data = json.loads(json_str)

        # 获取qxIndexNow值
        qx_index_now = data['result']['qxIndexNow']

        # 创建DataFrame
        df = pd.DataFrame({'emotion_index': [qx_index_now]})

        # 保存到CSV文件
        df.to_csv('data/emotion_index.csv', index=False, encoding='utf-8-sig')
