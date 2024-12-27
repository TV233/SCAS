import pandas as pd
from datetime import datetime, timedelta
import re
import os

def extract_month_day(date_str):
    """从日期字符串中提取月和日"""
    match = re.match(r'(\d{2})-(\d{2})', date_str)
    if not match:
        return None
    return tuple(map(int, match.groups()))

def create_date(month_day, year):
    """根据月日和年份创建日期"""
    try:
        return datetime(year, month_day[0], month_day[1])
    except ValueError:
        return None

def clean_comments(stock_code):
    """清洗指定股票的评论数据,只保留一年内的数据"""
    # 确保data目录存在
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 构建输入输出文件路径
    input_file = os.path.join(data_dir, f'comments_{stock_code}.csv')
    output_file = os.path.join(data_dir, f'comments_{stock_code}_clean.csv')
    
    if not os.path.exists(input_file):
        print(f"找不到股票{stock_code}的评论文件")
        return
        
    try:
        # 读取CSV文件
        df = pd.read_csv(input_file, encoding='utf-8')
        
        # 删除空的评论
        df = df.dropna(subset=['title'])
        
        # 获取当前年份
        current_year = datetime.now().year
        
        # 存储处理后的数据
        valid_rows = []
        dates = []
        
        # 记录第一条评论的月日
        first_month_day = None
        # 记录已经处理的行数
        processed_rows = 0
        # 设置检测循环的最小行数(经验值)
        MIN_ROWS_FOR_CYCLE = 1000
        
        # 获取第一行的月日作为最新日期
        if not df.empty:
            first_month_day = extract_month_day(df.iloc[0]['update_time'])
            if first_month_day:
                first_date = create_date(first_month_day, current_year)
                if first_date:
                    dates.append(first_date)
                    valid_rows.append(df.iloc[0])
        
        # 处理剩余行
        for idx, row in df.iloc[1:].iterrows():
            month_day = extract_month_day(row['update_time'])
            if not month_day:
                continue
                
            processed_rows += 1
            
            # 如果处理的行数超过最小值且遇到相同的月日，说明发生了循环
            if processed_rows > MIN_ROWS_FOR_CYCLE and month_day == first_month_day:
                break
                
            date = create_date(month_day, current_year)
            if date:
                dates.append(date)
                valid_rows.append(row)
        
        # 创建新的DataFrame，保持原始顺序
        clean_df = pd.DataFrame(valid_rows)
        
        # 保存结果
        clean_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"股票{stock_code}处理完成")
        print(f"原始数据行数: {len(df)}")
        print(f"清洗后数据行数: {len(clean_df)}")
        if dates:
            print(f"数据时间范围: {min(dates).strftime('%Y-%m-%d')} 到 {max(dates).strftime('%Y-%m-%d')}")
            print(f"处理的行数: {processed_rows}")
            
    except Exception as e:
        print(f"处理股票{stock_code}时出错: {e}")

def get_stock_codes():
    """从数据库获取股票代码列表"""
    from sqlalchemy import create_engine, text
    
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
        clean_comments(stock_code) 