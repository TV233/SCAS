import pandas as pd
from snownlp import SnowNLP
import os
from sqlalchemy import create_engine, text
from datetime import datetime
from stock_sentiment import StockSentiment

def analyze_sentiment(text):
    """使用改进的情感分析方法"""
    analyzer = StockSentiment()
    return analyzer.analyze(text)

def process_comments(stock_code):
    """处理指定股票的评论数据"""
    # 确保data目录存在
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 读取评论文件
    file_path = os.path.join(data_dir, f'comments_{stock_code}_clean.csv')
    if not os.path.exists(file_path):
        print(f"找不到股票{stock_code}的评论文件")
        return
        
    try:
        # 读取CSV文件，处理可能的编码问题
        data = pd.read_csv(file_path, encoding='utf-8')
        
        # 删除空的评论
        data = data.dropna(subset=['title'])
        
        # 对每句评论进行情感分析
        data['sentiment'] = data['title'].apply(analyze_sentiment)
        
        # 删除情感分析结果为空的行
        data = data.dropna(subset=['sentiment'])
        
        # 保存情感分析结果到CSV文件
        output_file = os.path.join(data_dir, f'emotionRating_{stock_code}.csv')
        data[['title', 'update_time', 'sentiment']].to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"股票{stock_code}的情感分析完成")
        
    except Exception as e:
        print(f"处理股票{stock_code}时出错: {e}")

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
