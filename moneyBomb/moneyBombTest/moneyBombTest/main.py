from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
# import mysql.connector
from sqlalchemy import create_engine, Table, MetaData, insert, delete
from sqlalchemy.sql import select
# import time
# from scrapy import cmdline
# import subprocess

settings = get_project_settings()
crawler = CrawlerProcess(settings)


def process_csv_to_mysql():
    print("将数据导入数据库...")
    # 读取CSV文件
    emotion_index_data = pd.read_csv('data/emotion_index.csv')
    market_style = pd.read_csv('data/market_style.csv')
    sectors_and_stocks = pd.read_csv('data/sectors_and_stocks.csv', dtype={'stock_code': str})
    top_text = pd.read_csv('data/top_text.csv')
    predict_data = pd.read_csv('data/predict.csv', dtype={'stock_code': str})
    stocks_data = pd.read_csv('data/stocks_data.csv', dtype={'stock_code': str})
    stock_indices = pd.read_csv('data/stock_indices.csv', dtype={'symbol': str})
    index_klines = pd.read_csv('data/index_klines.csv', dtype={'index_code': str})
    # 处理NaN值，将其转换为0
    predict_data.convert_dtypes()
    predict_data.fillna(value=0, inplace=True)
    # 将市场风格数据的dtype进行转换
    market_style.convert_dtypes()
    # 直接在原DataFrame上填充NaN值，不重新赋值
    market_style.fillna("", inplace=True)

    # MySQL数据库连接配置
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks',
        'raise_on_warnings': True
    }

    # 清空数据表
    def clear_table(table_name):
        table = metadata.tables[table_name]
        with engine.begin() as connection:
            connection.execute(delete(table))

    # 建立MySQL连接
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

    # 获取数据库元数据
    metadata = MetaData()
    metadata.reflect(bind=engine)
    # 清空所有相关的表
    print(
        "清空'emotion_index', 'market_style', 'sectors_and_stocks', 'top_text'表, 'stock_indices'表, 'index_klines'表")
    tables_to_clear = ['emotion_index', 'market_style', 'sectors_and_stocks', 'top_text', 'stock_indices',
                       'index_klines']
    for table_name in tables_to_clear:
        clear_table(table_name)

    print("导入'emotion_index'表")
    # emotion_index表中只有一个字段
    with engine.begin() as connection:
        # 准备插入数据到emotion_index表
        emotion_index_table = metadata.tables['emotion_index']
        with engine.begin() as connection:
            for index, row in emotion_index_data.iterrows():
                stmt = insert(emotion_index_table).values(emotion_index=row['emotion_index'])
                connection.execute(stmt)

    print("导入'market_style'表")
    # 反射market_style表
    market_style_table = Table('market_style', metadata, autoload_with=engine)

    with engine.begin() as connection:
        for index, row in market_style.iterrows():
            if row['change_rate'] == '':
                continue
            stmt = insert(market_style_table).values(  # name,change_rate,top_name
                name=row['name'],
                change_rate=row['change_rate'],
                top_name=row['top_name']
            )
            connection.execute(stmt)

    print("导入'sectors_and_stocks'表")
    # 反射sectors_and_stocks表 sector,reason,stock_code,stock_name
    sectors_and_stocks_table = Table('sectors_and_stocks', metadata, autoload_with=engine)
    with engine.begin() as connection:
        for index, row in sectors_and_stocks.iterrows():
            stmt = insert(sectors_and_stocks_table).values(
                sector=row['sector'],
                reason=row['reason'],
                stock_code=row['stock_code'],
                stock_name=row['stock_name']
            )
            connection.execute(stmt)

    print("导入'top_text'表")
    # 反射top_text表 position_index,title,content
    top_text_table = Table('top_text', metadata, autoload_with=engine)
    with engine.begin() as connection:
        for index, row in top_text.iterrows():
            stmt = insert(top_text_table).values(
                position_index=row['position_index'],
                title=row['title'],
                content=row['content']
            )
            connection.execute(stmt)

    print("导入'stock_indices'表")  # symbol,name,index_value,change_percent,change_amount
    stock_indices_table = Table('stock_indices', metadata, autoload_with=engine)
    with engine.begin() as connection:
        for index, row in stock_indices.iterrows():
            stmt = insert(stock_indices_table).values(
                symbol=row['symbol'],
                name=row['name'],
                index_value=row['index_value'],
                change_percent=row['change_percent'],
                change_amount=row['change_amount']
            )
            connection.execute(stmt)

    print("导入'index_klines'表")  # index_code,index_name,date_time,open,high,low,close,volume,value,last_close
    index_klines_table = Table('index_klines', metadata, autoload_with=engine)
    with engine.begin() as connection:
        for index, row in index_klines.iterrows():
            stmt = insert(index_klines_table).values(
                index_code=row['index_code'],
                index_name=row['index_name'],
                date_time=row['date_time'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume'],
                value=row['value'],
                last_close=row['last_close']
            )
            connection.execute(stmt)

    print("导入'stock_info'表")
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

    print("导入'stock_prices'表")
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
                stmt = stock_prices_table.update().where(
                    stock_prices_table.columns.stock_code == row['stock_code']).values(
                    latest_price=row['latest_price'],
                    price_change_rate=row['price_change_rate'],
                    price_change=row['price_change'],
                    rise_speed=row['rise_speed']
                )
            connection.execute(stmt)
    print("导入'predict'表")
    # 反射predict表
    predict_table = Table('predict', metadata, autoload_with=engine)
    # stock_code, RATING_ORG_NUM, RATING_BUY_NUM, RATING_ADD_NUM, RATING_NEUTRAL_NUM, RATING_REDUCE_NUM, RATING_SALE_NUM, YEAR1, EPS1, YEAR2, EPS2, YEAR3, EPS3, YEAR4, EPS4

    # 开始一个新的事务，更新predict表
    with engine.begin() as connection:
        for index, row in predict_data.iterrows():
            stmt = select(predict_table).where(predict_table.columns.stock_code == row['stock_code'])
            result = connection.execute(stmt)
            if result.fetchone() is None:
                # 如果这个股票代码在数据库中不存在，那么插入新条目
                stmt = insert(predict_table).values(
                    stock_code=row['stock_code'],
                    RATING_ORG_NUM=row['RATING_ORG_NUM'],
                    RATING_BUY_NUM=row['RATING_BUY_NUM'],
                    RATING_ADD_NUM=row['RATING_ADD_NUM'],
                    RATING_NEUTRAL_NUM=row['RATING_NEUTRAL_NUM'],
                    RATING_REDUCE_NUM=row['RATING_REDUCE_NUM'],
                    RATING_SALE_NUM=row['RATING_SALE_NUM'],
                    YEAR1=row['YEAR1'],
                    EPS1=row['EPS1'],
                    YEAR2=row['YEAR2'],
                    EPS2=row['EPS2'],
                    YEAR3=row['YEAR3'],
                    EPS3=row['EPS3'],
                    YEAR4=row['YEAR4'],
                    EPS4=row['EPS4']
                )
            else:
                # 如果这个股票代码在数据库中已经存在，那么更新这个条目
                stmt = predict_table.update().where(
                    predict_table.columns.stock_code == row['stock_code']).values(
                    RATING_ORG_NUM=row['RATING_ORG_NUM'],
                    RATING_BUY_NUM=row['RATING_BUY_NUM'],
                    RATING_ADD_NUM=row['RATING_ADD_NUM'],
                    RATING_NEUTRAL_NUM=row['RATING_NEUTRAL_NUM'],
                    RATING_REDUCE_NUM=row['RATING_REDUCE_NUM'],
                    RATING_SALE_NUM=row['RATING_SALE_NUM'],
                    YEAR1=row['YEAR1'],
                    EPS1=row['EPS1'],
                    YEAR2=row['YEAR2'],
                    EPS2=row['EPS2'],
                    YEAR3=row['YEAR3'],
                    EPS3=row['EPS3'],
                    YEAR4=row['YEAR4'],
                    EPS4=row['EPS4']
                )
            connection.execute(stmt)


    # 关闭连接
    engine.dispose()

    print("导入结束")


if __name__ == '__main__':
    print("爬虫启动................")

    print("开始爬取")

    crawler.crawl('getStocksData')
    crawler.crawl('getEmotionIndex')
    crawler.crawl('getPositionInfo')
    crawler.crawl('getPredict')
    crawler.crawl('getMainIndex')
    crawler.crawl('getIndexKlines')
    # crawler.crawl('getComment')
    crawler.start()

    print("爬取完成")

    process_csv_to_mysql()

    print("爬虫结束................")
