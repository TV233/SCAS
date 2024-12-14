import json
import pandas as pd
import scrapy
import os


class GetStockKline(scrapy.Spider):
    print("爬取股票K线数据")
    name = "getStockKline"

    def start_requests(self):
        # 读取stocks_data.csv文件获取股票代码列表
        csv_path = 'data/stocks_data.csv'
        if not os.path.exists(csv_path):
            self.log('stocks_data.csv文件不存在')
            return
            
        df = pd.read_csv(csv_path)
        stock_codes = df['stock_code'].astype(str).tolist()
        
        base_url = ("https://push2his.eastmoney.com/api/qt/stock/kline/get?"
                   "fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&"
                   "fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&"
                   "beg=20230101&end=20500101&rtntype=6&secid={}.{}&klt=101&fqt=1")

        # 确保data目录存在
        if not os.path.exists('data'):
            os.makedirs('data')

        # 遍历所有股票代码生成请求
        for stock_code in stock_codes:
            # 补齐6位股票代码
            stock_code = stock_code.zfill(6)
            
            # 根据股票代码判断市场类型
            # 上海市场股票代码以'6'开头，深圳市场股票代码以'0'或'3'开头
            market_type = '1' if stock_code.startswith('6') else '0'
            
            url = base_url.format(market_type, stock_code)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'stock_code': stock_code}
            )

    def __init__(self, *args, **kwargs):
        super(GetStockKline, self).__init__(*args, **kwargs)
        self.data_frames = {}  # 用字典存储每个股票的DataFrame

    def parse(self, response):
        stock_code = response.meta['stock_code']
        
        try:
            # 解析返回的JSON数据
            json_data = json.loads(response.text)
            
            if 'data' in json_data and json_data['data'] and 'klines' in json_data['data']:
                stock_data = json_data['data']
                klines_data = stock_data['klines']
                klines = []
                
                for kline in klines_data:
                    # 解析每一条K线数据
                    (
                        date_time, open_price, close_price, high_price, low_price, volume,
                        value, amplitude, up_down_range, up_down_price, turnover_rate
                    ) = kline.split(',')

                    klines.append({
                        'stock_code': stock_code,
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

                if klines:
                    # 创建DataFrame并保存为CSV文件
                    df = pd.DataFrame(klines)
                    file_name = f'data/klines/{stock_data["market"]}_{stock_data["code"]}_klines.csv'
                    df.to_csv(
                        file_name,
                        index=False,
                        encoding='utf-8-sig',
                        float_format='%.2f'  # 保留2位小数
                    )
                    self.log(f'已保存{stock_code}的K线数据到{file_name}')
            else:
                self.log(f'股票{stock_code}没有K线数据')
                
        except Exception as e:
            self.log(f'处理股票{stock_code}的数据时出错: {str(e)}')
