from sqlalchemy import create_engine, Table, MetaData, insert, delete
import pandas as pd
import os
from datetime import datetime

def update_stock_klines():
    print("开始更新K线数据...")
    
    # MySQL数据库连接配置
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks',
        'raise_on_warnings': True
    }

    # 建立MySQL连接
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

    # 获取数据库元数据
    metadata = MetaData()
    metadata.reflect(bind=engine)

    print("清空'stock_kline'表")
    # 清空stock_kline表
    stock_kline_table = Table('stock_kline', metadata, autoload_with=engine)
    with engine.begin() as connection:
        connection.execute(delete(stock_kline_table))
    
    # 读取klines目录下的所有K线数据文件
    klines_dir = 'data/klines'
    if not os.path.exists(klines_dir):
        print(f"K线数据目录 {klines_dir} 不存在")
        return
        
    # 使用���量插入来提高性能
    batch_size = 1000  # 每批处理的记录数
    total_records = 0
    
    try:
        with engine.begin() as connection:
            for filename in os.listdir(klines_dir):
                if filename.endswith('_klines.csv'):
                    file_path = os.path.join(klines_dir, filename)
                    print(f"正在处理文件: {filename}")
                    
                    try:
                        # 读取CSV文件，确保stock_code作为字符串读取
                        df = pd.read_csv(file_path, dtype={'stock_code': str})
                        
                        # 将date_time列转换为datetime格式
                        df['date_time'] = pd.to_datetime(df['date_time'])
                        
                        # 批量处理数据
                        records = df.to_dict('records')
                        batch = []
                        
                        for record in records:
                            batch.append({
                                'stock_code': record['stock_code'],
                                'date_time': record['date_time'].date(),
                                'open_price': record['open_price'],
                                'close_price': record['close_price'],
                                'high_price': record['high_price'],
                                'low_price': record['low_price'],
                                'volume': record['volume'],
                                'trade_value': record['trade_value'],
                                'amplitude': record['amplitude'],
                                'up_down_range': record['up_down_range'],
                                'up_down_price': record['up_down_price'],
                                'turnover_rate': record['turnover_rate']
                            })
                            
                            # 当batch达到指定大小时执行插入
                            if len(batch) >= batch_size:
                                connection.execute(insert(stock_kline_table), batch)
                                total_records += len(batch)
                                print(f"已处理 {total_records} 条记录")
                                batch = []
                        
                        # 处理剩余的记录
                        if batch:
                            connection.execute(insert(stock_kline_table), batch)
                            total_records += len(batch)
                            print(f"已处理 {total_records} 条记录")
                            
                    except Exception as e:
                        print(f"处理文件 {filename} 时出错: {str(e)}")
                        continue
                        
        print(f"K线数据导入完成，共导入 {total_records} 条记录")
        
    except Exception as e:
        print(f"更新K线数据时发生错误: {str(e)}")
    finally:
        engine.dispose()

if __name__ == '__main__':
    update_stock_klines() 