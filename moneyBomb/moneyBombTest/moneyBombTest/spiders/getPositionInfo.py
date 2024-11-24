import json
import pandas as pd
import scrapy


class GetstockcodeSpider(scrapy.Spider):
    print("爬取仓位数据MarketStyle/TopText/sectors_and_stocks")
    name = "getPositionInfo"
    # allowed_domains = ["quote.eastmoney.com"]
    start_urls = ["https://quote.eastmoney.com/ztb/api/cangweiinfos"]

    def parse(self, response):
        # print(response.text)
        jsonp_data = response.text
        print(jsonp_data)
        # 去掉前后的非JSON部分
        json_str = jsonp_data[jsonp_data.index('{'):jsonp_data.rindex('}') + 1]

        # 解析JSON数据
        data = json.loads(json_str)

        # 初始化列表存储所有需要的数据
        top_texts = []
        sectors_and_stocks = []

        # 提取数据
        for item in data['result']:
            # 提取TopText并添加到列表
            top_text = item['TopText']
            top_texts.append({
                'position_index': top_text['PositionInd'],
                'title': top_text['Title'],
                'content': top_text['Content']
            })

            # 遍历所有推荐中的ThemeList
            for recommend in item['Recommend']:
                for theme in recommend['ThemeList']:
                    for stock in theme['StockList']:
                        sectors_and_stocks.append({
                            'sector': theme['Name'],
                            'reason': theme['Reason'],
                            'stock_code': stock['Code'],
                            'stock_name': stock['Name']
                        })
        # 初始化列表存储MarketStyle数据
        market_styles = []

        # 提取MarketStyle数据
        for result in data['result']:
            for category in result.get('MarketStyle', []):
                for theme in category['ThemeList']:
                    market_styles.append({
                        'name': theme['Name'],
                        'change_rate': theme['Chg'],
                        'top_name': theme['TopName'] if theme['TopName'] else 'N/A'  # 提供默认值为 'N/A' 如果TopName为空
                    })

        # 将MarketStyle信息保存到CSV
        df_market_styles = pd.DataFrame(market_styles)
        df_market_styles.to_csv('data/market_style.csv', index=False, encoding='utf-8-sig')
        # 将TopText信息保存到CSV
        df_top_text = pd.DataFrame(top_texts)
        df_top_text.to_csv('data/top_text.csv', index=False, encoding='utf-8-sig')
        # 将Sector, Reason, StockCode, StockName信息保存到CSV
        df_sectors_stocks = pd.DataFrame(sectors_and_stocks)
        df_sectors_stocks.to_csv('data/sectors_and_stocks.csv', index=False, encoding='utf-8-sig')
