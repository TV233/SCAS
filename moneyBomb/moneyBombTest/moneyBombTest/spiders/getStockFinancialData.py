import json
import pandas as pd
import scrapy


class GetStockFinancialDataSpider(scrapy.Spider):
    name = "getStockFinancialData"
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8-sig'  # Ensure proper encoding for CSV
    }

    def start_requests(self):
        # 读取CSV文件以获取股票代码列表
        stocks_df = pd.read_csv('data/stocks.csv')
        # 确保股票代码是字符串格式，前导零被保留
        stock_codes = stocks_df['stock_code'].apply(lambda x: f"{int(x):06d}").tolist()

        # 构建每个股票财报的URL并发起请求
        for code in stock_codes:
            url = f"https://bdstatics.eastmoney.com/web/prd/reportData/2023Q3/{code}.json"
            yield scrapy.Request(url=url, callback=self.parse, meta={'stock_code': code})

    def parse(self, response):
        # 获取股票代码
        stock_code = response.meta['stock_code']

        # 解析JSON数据
        json_data = json.loads(response.text)

        # 准备数据列表
        data_list = []

        # 从JSON字典中提取数据
        if 'FR_REV' in json_data and 'FR_PARENTPROFIT' in json_data and 'FR_DNETPROFIT' in json_data:
            for year_data in zip(json_data['FR_REV'], json_data['FR_PARENTPROFIT'], json_data['FR_DNETPROFIT']):
                total_operate_reve = year_data[0]
                parent_net_profit = year_data[1]
                d_net_profit_atpc = year_data[2]

                data_list.append({
                    "stock_code": stock_code,
                    "Year": total_operate_reve.get("X_AXIS", "N/A"),
                    "total_operatereve_increase": total_operate_reve.get("TOTALOPERATEREVE_INCREASE", 0),
                    "parent_netprofit_increase": parent_net_profit.get("PARENTNETPROFIT_INCREASE", 0),
                    "dnetprofitatpc_tcal_increase": d_net_profit_atpc.get("DNETPROFITATPC_TCAL_INCREASE", 0),
                    "summary": json_data['FR_SHAREWORD']['TITLE'] if 'FR_SHAREWORD' in json_data else "No Summary"
                })

        # 创建DataFrame
        df = pd.DataFrame(data_list)
        print(df)
        # 判断文件是否存在以决定是否写入头部
        import os
        file_exists = os.path.isfile('data/financial_data.csv')

        # 保存到CSV文件，使用追加模式
        df.to_csv('data/financial_data.csv', mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
