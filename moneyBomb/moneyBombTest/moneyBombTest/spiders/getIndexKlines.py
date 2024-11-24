import json
import pandas as pd
import scrapy


class GetstockcodeSpider(scrapy.Spider):
    print("爬取股票指数K线getIndexKlines")
    name = "getIndexKlines"

    def start_requests(self):
        # 定义不同的secid对应不同的股票指数
        secids = ["1.000001", "0.399001", "0.399006", "1.000300"]
        base_url = "https://push2.eastmoney.com/api/qt/stock/trends2/get"

        for secid in secids:
            url = (f"{base_url}?secid={secid}&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,"
                   f"f54,f55,f56,f57,f58")
            yield scrapy.Request(url, self.parse, meta={'secid': secid})

    def __init__(self, *args, **kwargs):
        super(GetstockcodeSpider, self).__init__(*args, **kwargs)
        self.data_frame = pd.DataFrame()  # 初始化空的DataFrame

    def parse(self, response):
        # print(response.text)
        jsonp_data = response.text
        print(jsonp_data)
        # 去掉前后的非JSON部分
        json_str = jsonp_data[jsonp_data.index('{'):jsonp_data.rindex('}') + 1]

        # 解析JSON数据
        data = json.loads(json_str)
        index_data = data['data']

        # 提取K线数据
        klines = []
        for trend in index_data['trends']:
            date_time, open_price, high_price, low_price, close_price, volume, value, last_close = trend.split(',')
            klines.append({
                'index_code': index_data['code'],
                'index_name': index_data['name'],
                'date_time': date_time,
                'open': float(open_price),
                'high': float(high_price),
                'low': float(low_price),
                'close': float(close_price),
                'volume': int(volume),
                'value': float(value),
                'last_close': float(last_close)
            })


        # 创建DataFrame并将数据添加到爬虫的DataFrame中
        new_data = pd.DataFrame(klines)
        self.data_frame = pd.concat([self.data_frame, new_data], ignore_index=True)
        self.data_frame.to_csv('data/index_klines.csv', index=False, encoding='utf-8-sig')
