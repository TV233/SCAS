import json
import pandas as pd
import scrapy


class GetStockKline(scrapy.Spider):
    print("爬取股票K线数据")
    name = "getStockKline"

    def start_requests(self):
        # secid 是股票的代码，1表示上证，0表示深证。例如 1.601360 代表某股票
        self.stock_code = "601360"  # 存储股票代码
        secid = f"1.{self.stock_code}"  # 替换成你需要爬取的股票代码
        base_url = ("https://push2his.eastmoney.com/api/qt/stock/kline/get?"
                    "fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&"
                    "fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&"
                    "beg=20230101&end=20500101&rtntype=6&secid={}&klt=101&fqt=1")

        url = base_url.format(secid)
        yield scrapy.Request(url, self.parse)

    def __init__(self, *args, **kwargs):
        super(GetStockKline, self).__init__(*args, **kwargs)
        self.data_frame = pd.DataFrame()  # 初始化空的DataFrame

    def parse(self, response):
        # 解析返回的JSON数据
        json_data = json.loads(response.text)
        if 'data' in json_data and 'klines' in json_data['data']:
            stock_data = json_data['data']
            klines_data = stock_data['klines']
            klines = []
            for kline in klines_data:
                # 根据新的数据格式解析每一条K线数据
                (
                    date_time, open_price, close_price, high_price, low_price, volume,
                    value, amplitude, up_down_range, up_down_price, turnover_rate
                ) = kline.split(',')

                klines.append({
                    'stock_code': self.stock_code,
                    'date_time': date_time,
                    'open_price': float(open_price),
                    'close_price': float(close_price),
                    'high_price': float(high_price),
                    'low_price': float(low_price),
                    'volume': int(volume),
                    'trade_value': float(value),
                    'amplitude': float(amplitude),
                    'up_down_range': float(up_down_range),
                    'up_down_price': float(up_down_price),
                    'turnover_rate': float(turnover_rate)
                })

            # 创建DataFrame并将数据添加到爬虫的DataFrame中
            new_data = pd.DataFrame(klines)
            self.data_frame = pd.concat([self.data_frame, new_data], ignore_index=True)

            # 将数据保存为CSV文件
            self.data_frame.to_csv(
                f'data/{stock_data["market"]}_{stock_data["code"]}_klines.csv',
                index=False,
                encoding='utf-8-sig',
                float_format='%.2f'  # 保留2位小数
            )
        else:
            self.log('No data found for this stock.')
