import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, insert, delete, text
from datetime import datetime
import os

def generate_sentiment_trend(stock_code):
    """生成指定股票的情感趋势数据"""
    # 确保data目录存在
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 读取情感分析结果
    file_path = os.path.join(data_dir, f'emotionRating_{stock_code}.csv')
    if not os.path.exists(file_path):
        print(f"找不到股票{stock_code}的情感分析文件")
        return
        
    df = pd.read_csv(file_path)
    
    # 转换评论时间格式，根据月份判断年份
    def get_date_with_year(date_str):
        month = int(date_str.split('-')[0])
        # 如果月份是1-10月，年份是2024年；如果是11-12月，年份是2023年
        year = 2024 if month <= 10 else 2023
        return pd.to_datetime(f'{year}-{date_str}', format='%Y-%m-%d %H:%M')
    
    df['comment_date'] = df['update_time'].apply(get_date_with_year)
    
    # 按日期分组计算平均情感值
    daily_sentiment = df.groupby(df['comment_date'].dt.date)['sentiment'].agg(['mean', 'count']).reset_index()
    
    # 保存到数据库
    save_to_database(daily_sentiment, stock_code)

def save_to_database(sentiment_data, stock_code):
    """保存情感趋势数据到数据库"""
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks'
    }
    
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    try:
        sentiment_trend_table = Table('sentiment_trend', metadata, autoload_with=engine)
        
        # 删除该股票的旧数据
        with engine.begin() as connection:
            connection.execute(
                delete(sentiment_trend_table).where(sentiment_trend_table.c.stock_code == stock_code)
            )
        
        # 插入新数据
        current_time = datetime.now()
        with engine.begin() as connection:
            for _, row in sentiment_data.iterrows():
                stmt = insert(sentiment_trend_table).values(
                    stock_code=stock_code,
                    date=row['comment_date'],
                    sentiment_avg=float(row['mean']),
                    comment_count=int(row['count']),
                    update_time=current_time
                )
                connection.execute(stmt)
                
    except Exception as e:
        print(f"数据库操作错误: {e}")
    finally:
        engine.dispose()

def get_stock_codes():
    """从数据库获取股票代码列表"""
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks'
    }
    
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT stock_code FROM stock_info"))
            return [row[0] for row in result]
    except Exception as e:
        print(f"获取股票代码失败: {e}")
        return []
    finally:
        engine.dispose()

if __name__ == '__main__':
    stock_codes = get_stock_codes()
    if not stock_codes:
        print("没有获取到股票代码")
        exit(1)
        
    for stock_code in stock_codes:
        generate_sentiment_trend(stock_code) 