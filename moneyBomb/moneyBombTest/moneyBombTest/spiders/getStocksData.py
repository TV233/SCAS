import json
import pandas as pd
import scrapy


class GetstockcodeSpider(scrapy.Spider):
    print("爬取StocksData/StocksInfo")
    name = "getStocksData"
    # allowed_domains = ["quote.eastmoney.com"]
    start_urls = [
        "https://3.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112409852962385529274_1710596785775&pn=1&pz=10000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1710596785777"]

    def parse(self, response):
        # print(response.text)
        jsonp_data = response.text
        # print(jsonp_data)
        # 去掉前后的非JSON部分
        json_str = jsonp_data[jsonp_data.index('{'):jsonp_data.rindex('}') + 1]

        # 解析JSON数据
        data = json.loads(json_str)

        # 提取需要的字段
        data_list = data['data']['diff']
        filtered_data = [{'stock_code': item.get('f12', None),
                          'stock_name': item.get('f14', None),
                          'latest_price': item.get('f2', None),
                          'price_change_rate': item.get('f3', None),
                          'price_change': item.get('f4', None),
                          'rise_speed': item.get('f22', None)}
                         for item in data_list
                         if all(item.get(field) != '-' for field in ['f2', 'f3', 'f4', 'f22'])]

        # 当一只股票退市时，后面四个字段都为“-”，将其过滤

        # 将结果保存到CSV文件
        df = pd.DataFrame(filtered_data)
        df.to_csv('data/stocks_data.csv', index=False)
        pass
