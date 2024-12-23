import pandas as pd
import jieba
from collections import Counter
import re
from sqlalchemy import create_engine, Table, MetaData, insert, delete, text
from datetime import datetime
import os

def clean_text(text):
    """清理文本"""
    text = re.sub(r'\[.*?\]', '', text)  # 移除[xxx]格式的表情
    text = re.sub(r'[^\w\s]', '', text)  # 只保留字母、数字和空格
    return text

def generate_word_frequency(stock_code):
    """生成指定股票的词频统计"""
    # 确保data目录存在
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 读取评论文件
    file_path = os.path.join(data_dir, f'comments_{stock_code}.csv')
    if not os.path.exists(file_path):
        print(f"找不到股票{stock_code}的评论文件")
        return
        
    df = pd.read_csv(file_path)
    
    # 清洗和分词
    text_list = []
    for text in df['title']:
        cleaned_text = clean_text(str(text))
        words = jieba.cut(cleaned_text)
        text_list.extend([word for word in words if len(word) > 1])
    
    # 统计词频
    word_freq = Counter(text_list)
    
    # 获取前100个高频词及其频率
    top_words = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:100])
    
    # 保存到数据库
    save_to_database(top_words, stock_code)

def save_to_database(word_freq, stock_code):
    """保存词频数据到数据库"""
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
        word_frequency_table = Table('word_frequency', metadata, autoload_with=engine)
        
        # 删除该股票的旧数据
        with engine.begin() as connection:
            connection.execute(
                delete(word_frequency_table).where(word_frequency_table.c.stock_code == stock_code)
            )
        
        # 插入新数据
        current_time = datetime.now()
        with engine.begin() as connection:
            for word, freq in word_freq.items():
                stmt = insert(word_frequency_table).values(
                    stock_code=stock_code,
                    word=word,
                    frequency=freq,
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
        generate_word_frequency(stock_code) 