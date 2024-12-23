import pandas as pd
from snownlp import SnowNLP
import os
from sqlalchemy import create_engine, text
from datetime import datetime

def process_comments(stock_code):
    """处理指定股票的评论数据"""
    # 确保data目录存在
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 读取评论文件
    file_path = os.path.join(data_dir, f'comments_{stock_code}.csv')
    if not os.path.exists(file_path):
        print(f"找不到股票{stock_code}的评论文件")
        return
        
    data = pd.read_csv(file_path)
    
    # 对每句评论进行情感分析
    data['sentiment'] = data['title'].apply(lambda x: SnowNLP(x).sentiments)
    
    # 保存情感分析结果到CSV文件
    output_file = os.path.join(data_dir, f'emotionRating_{stock_code}.csv')
    data[['title', 'update_time', 'sentiment']].to_csv(output_file, index=False)
    
    print(f"股票{stock_code}的情感分析完成")

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
        process_comments(stock_code)
