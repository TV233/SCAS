import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, Table, MetaData, insert
from sqlalchemy.sql import select

print("将数据导入数据库...")
# 读取CSV文件
# primary_business_component_analysis = pd.reacsv2mysql.pyd_csv('primary_business_component_analysis.csv')
# primary_business_field = pd.read_csv('primary_business_field.csv')
# business_review = pd.read_csv('business_review.csv')
emotion_index_data = pd.read_csv('emotion_index.csv')
market_style = pd.read_csv('market_style.csv')
sectors_and_stocks = pd.read_csv('sectors_and_stocks.csv')
stock_info = pd.read_csv('stock.csv', dtype={'stock_code': str})
top_text = pd.read_csv('top_text.csv')
predict_data = pd.read_csv('predict.csv', dtype={'stock_code': str})
stocks_data = pd.read_csv('stocks_data.csv', dtype={'stock_code': str})
predict_data = pd.read_csv('predict.csv', dtype={'stock_code': str})
# 处理NaN值，将其转换为None
predict_data = predict_data.convert_dtypes()
predict_data = predict_data.where(pd.notnull(predict_data), None)
# MySQL数据库连接配置
db_config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'database': 'stocks',
    'raise_on_warnings': True
}

# 建立MySQL连接
engine = create_engine(
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

# 将数据写入MySQL数据库
# primary_business_component_analysis.to_sql(name='primary_business_component_analysis', con=engine, if_exists='append',
#                                            index=False)
# primary_business_field.to_sql(name='primary_business_field', con=engine, if_exists='append', index=False)
# business_review.to_sql(name='business_review', con=engine, if_exists='append', index=False)
# stocks_data.to_sql(name='stocks_data', con=engine, if_exists='append', index=False)
# 获取数据库元数据
metadata = MetaData()

# 反射stock_info表
stock_info_table = Table('stock_info', metadata, autoload_with=engine)

# 开始一个新的事务，先更新stock_info表
with engine.begin() as connection:
    for index, row in stocks_data.iterrows():
        # 检查这个股票代码是否已经在数据库中存在
        stmt = select(stock_info_table).where(stock_info_table.columns.stock_code == row['stock_code'])
        result = connection.execute(stmt)
        if result.fetchone() is None:
            # 如果这个股票代码在数据库中不存在，那么插入新条目
            stmt = insert(stock_info_table).values(
                stock_code=row['stock_code'],
                stock_name=row['stock_name']
            )
        else:
            # 如果这个股票代码在数据库中已经存在，那么更新这个条目
            stmt = stock_info_table.update().where(stock_info_table.columns.stock_code == row['stock_code']).values(
                stock_name=row['stock_name']
            )
        connection.execute(stmt)

# 反射stock_prices表
stock_prices_table = Table('stock_prices', metadata, autoload_with=engine)

# 开始一个新的事务，更新stock_prices表
with engine.begin() as connection:
    for index, row in stocks_data.iterrows():
        # 检查这个股票代码是否已经在数据库中存在
        stmt = select(stock_prices_table).where(stock_prices_table.columns.stock_code == row['stock_code'])
        result = connection.execute(stmt)
        if result.fetchone() is None:
            # 如果这个股票代码在数据库中不存在，那么插入新条目
            stmt = insert(stock_prices_table).values(
                stock_code=row['stock_code'],
                latest_price=row['latest_price'],
                price_change_rate=row['price_change_rate'],
                price_change=row['price_change'],
                rise_speed=row['rise_speed']
            )
        else:
            # 如果这个股票代码在数据库中已经存在，那么更新这个条目
            stmt = stock_prices_table.update().where(stock_prices_table.columns.stock_code == row['stock_code']).values(
                latest_price=row['latest_price'],
                price_change_rate=row['price_change_rate'],
                price_change=row['price_change'],
                rise_speed=row['rise_speed']
            )
        connection.execute(stmt)

# 反射predict表
predict_table = Table('predict', metadata, autoload_with=engine)

# 开始一个新的事务，更新predict表
with engine.begin() as connection:
    for index, row in predict_data.iterrows():
        # Check if this stock_code exists in the stock_info table
        stmt = select(stock_info_table).where(stock_info_table.columns.stock_code == row['stock_code'])
        result = connection.execute(stmt)
        if result.fetchone() is not None:
            # If the stock_code exists in stock_info, insert new entry into predict table
            stmt = insert(predict_table).values(**row.to_dict())
            connection.execute(stmt)

# 关闭连接
engine.dispose()

# # 反射primary_business_component_analysis表
# table = Table('primary_business_component_analysis', metadata, autoload_with=engine)
#
# # 开始一个新的事务
# with engine.begin() as connection:
#     for index, row in primary_business_component_analysis.iterrows():
#         # 检查这个股票代码是否已经在数据库中存在
#         stmt = select(table).where(table.columns.stock_code == row['stock_code'])
#         result = connection.execute(stmt)
#         if result.fetchone() is None:
#             # 如果这个股票代码在数据库中不存在，那么插入新条目
#             stmt = insert(table).values(
#                 stock_code_with_exchange=row['stock_code_with_exchange'],
#                 stock_code=row['stock_code'],
#                 report_date=row['report_date'],
#                 mainop_type=row['mainop_type'],
#                 item_name=row['item_name'],
#                 main_business_income=row['main_business_income'],
#                 mbi_ratio=row['mbi_ratio'],
#                 rank=row['rank'],
#                 main_business_cost=row['main_business_cost'],
#                 mbc_ratio=row['mbc_ratio'],
#                 main_business_profit=row['main_business_profit'],
#                 mbr_ratio=row['mbr_ratio'],
#                 gross_profit_ratio=row['gross_profit_ratio']
#             )
#         else:
#             # 如果这个股票代码在数据库中已经存在，那么更新这个条目
#             stmt = table.update().where(table.columns.stock_code == row['stock_code']).values(
#                 stock_code_with_exchange=row['stock_code_with_exchange'],
#                 stock_code=row['stock_code'],
#                 report_date=row['report_date'],
#                 mainop_type=row['mainop_type'],
#                 item_name=row['item_name'],
#                 main_business_income=row['main_business_income'],
#                 mbi_ratio=row['mbi_ratio'],
#                 rank=row['rank'],
#                 main_business_cost=row['main_business_cost'],
#                 mbc_ratio=row['mbc_ratio'],
#                 main_business_profit=row['main_business_profit'],
#                 mbr_ratio=row['mbr_ratio'],
#                 gross_profit_ratio=row['gross_profit_ratio']
#             )
#         connection.execute(stmt)
#
# # 关闭连接
#
# engine.dispose()
#
#
# # 反射primary_business_field表
# table = Table('primary_business_field', metadata, autoload_with=engine)
#
# # 开始一个新的事务
# with engine.begin() as connection:
#     for index, row in primary_business_field.iterrows():
#         # 检查这个股票代码是否已经在数据库中存在
#         stmt = select(table).where(table.columns.stock_code == row['stock_code'])
#         result = connection.execute(stmt)
#         if result.fetchone() is None:
#             # 如果这个股票代码在数据库中不存在，那么插入新条目
#             stmt = insert(table).values(
#                 stock_code_with_exchange=row['stock_code_with_exchange'],
#                 stock_code=row['stock_code'],
#                 business_scope=row['business_scope']
#             )
#         else:
#             # 如果这个股票代码在数据库中已经存在，那么更新这个条目
#             stmt = table.update().where(table.columns.stock_code == row['stock_code']).values(
#                 stock_code_with_exchange=row['stock_code_with_exchange'],
#                 stock_code=row['stock_code'],
#                 business_scope=row['business_scope']
#             )
#         connection.execute(stmt)
#
# # 关闭连接
#
# engine.dispose()
#
#
# # 反射business_review表
# table = Table('business_review', metadata, autoload_with=engine)
# #stock_code_with_exchange,stock_code,report_date,business_review
# # 开始一个新的事务
# with engine.begin() as connection:
#     for index, row in business_review.iterrows():
#         # 检查这个股票代码是否已经在数据库中存在
#         stmt = select(table).where(table.columns.stock_code == row['stock_code'])
#         result = connection.execute(stmt)
#         if result.fetchone() is None:
#             # 如果这个股票代码在数据库中不存在，那么插入新条目
#             stmt = insert(table).values(
#                 stock_code_with_exchange=row['stock_code_with_exchange'],
#                 stock_code=row['stock_code'],
#                 report_date=row['report_date'],
#                 business_review = row['business_review']
#             )
#         else:
#             # 如果这个股票代码在数据库中已经存在，那么更新这个条目
#             stmt = table.update().where(table.columns.stock_code == row['stock_code']).values(
#                 stock_code_with_exchange=row['stock_code_with_exchange'],
#                 stock_code=row['stock_code'],
#                 report_date=row['report_date'],
#                 business_review = row['business_review']
#             )
#         connection.execute(stmt)
#
# # 关闭连接
#
# engine.dispose()

print("导入结束")
