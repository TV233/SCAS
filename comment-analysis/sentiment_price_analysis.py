import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Table, MetaData, Column, String, Float, Date, DateTime, Integer, text
from datetime import datetime
import os
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import pearsonr
import logging

# 设置日志
def setup_logger():
    """配置日志"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, f'sentiment_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    
    return logging.getLogger(__name__)

def create_analysis_table():
    """创建情感-股价关系分析表"""
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks'
    }
    
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    
    metadata = MetaData()
    
    # 创建情感-股价关系分析表
    Table('sentiment_price_correlation', metadata,
        Column('stock_code', String(20), primary_key=True),
        Column('date', Date, primary_key=True),
        Column('sentiment_change', Float),  # 情感值变化
        Column('price_change', Float),      # 股价变动百分比
        Column('correlation', Float),        # 相关系数
        Column('sentiment_count', Integer),  # 情感评论数量
        Column('is_significant', Integer),   # 相关性是否显著(p值<0.05)
        Column('correlation_summary', String(255)),  # 相关性分析总结
        Column('update_time', DateTime)
    )
    
    try:
        metadata.create_all(engine)
        return True
    except Exception as e:
        logger.error(f"创建数据表时出错: {e}", exc_info=True)
        return False
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
        logger.error(f"获取股票代码失败: {e}", exc_info=True)
        return []
    finally:
        engine.dispose()

def get_kline_data(stock_code, engine):
    """从数据库获取K线数据"""
    try:
        query = text("""
            SELECT 
                date_time as date,
                close_price
            FROM stock_kline 
            WHERE stock_code = :code
            ORDER BY date_time
        """)
        
        df = pd.read_sql(query, engine, params={'code': stock_code})
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # 计算价格变化百分比
        df['price_change'] = df['close_price'].pct_change() * 100
        
        return df
        
    except Exception as e:
        logger.error(f"获取股票{stock_code}的K线数据时出错: {e}", exc_info=True)
        return None

def analyze_sentiment_price_relation(stock_code, logger):
    """分析特定股票的情感与股价关系"""
    # 读取情感数据
    sentiment_file = os.path.join(os.path.dirname(__file__), 'data', f'emotionRating_{stock_code}.csv')
    if not os.path.exists(sentiment_file):
        logger.error(f"找不到股票{stock_code}的情感数据文件: {sentiment_file}")
        return
    
    # 创建数据库连接
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks'
    }
    
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    
    try:
        # 读取数据
        sentiment_df = pd.read_csv(sentiment_file)
        kline_df = get_kline_data(stock_code, engine)
        
        if kline_df is None or kline_df.empty:
            logger.error(f"无法获取股票{stock_code}的K线数据")
            return
        
        logger.info(f"股票{stock_code}数据读取成功:")
        logger.info(f"- 情感数据: {len(sentiment_df)}条")
        logger.info(f"- K线数据: {len(kline_df)}条")
        
        # 处理日期格式
        def get_date_with_year(date_str):
            try:
                date_parts = date_str.split(' ')[0]
                month, day = map(int, date_parts.split('-'))
                current_year = datetime.now().year
                current_month = datetime.now().month
                current_day = datetime.now().day
                year = current_year - 1 if (month >= current_month and day > current_day) else current_year
                return pd.to_datetime(f'{year}-{date_str}', format='%Y-%m-%d %H:%M').date()
            except Exception as e:
                logger.error(f"日期转换错误: {date_str}, 错误: {e}")
                return None
        
        sentiment_df['date'] = sentiment_df['update_time'].apply(get_date_with_year)
        
        # 计算每日平均情感值
        daily_sentiment = sentiment_df.groupby('date').agg({
            'sentiment': ['mean', 'count']
        }).reset_index()
        daily_sentiment.columns = ['date', 'sentiment_avg', 'sentiment_count']
        
        # 对情感值进行排序，确保按日期顺序计算变化
        daily_sentiment = daily_sentiment.sort_values('date')
        
        # 计算情感值的变化（今天的情感值 - 昨天的情感值）
        daily_sentiment['sentiment_change'] = daily_sentiment['sentiment_avg'].diff()
        
        # 输出一些调试信息
        logger.info("情感数据示例:")
        logger.info(daily_sentiment[['date', 'sentiment_avg', 'sentiment_change', 'sentiment_count']].head())
        
        # 合并数据，使用当天的股价变化
        merged_df = pd.merge(daily_sentiment, 
                           kline_df[['date', 'price_change']], 
                           on='date', how='inner')
        
        # 删除缺失值和异常值
        merged_df = merged_df.dropna(subset=['sentiment_change', 'price_change'])
        
        # 输出合并后的数据示例
        logger.info("\n合并后的数据示例:")
        logger.info(merged_df[['date', 'sentiment_change', 'price_change', 'sentiment_count']].head())
        
        # 计算相关系数和显著性
        correlation, p_value = pearsonr(merged_df['sentiment_change'], 
                                      merged_df['price_change'])
        
        logger.info(f"\n相关性分析结果:")
        logger.info(f"- 相关系数: {correlation:.3f}")
        logger.info(f"- P值: {p_value:.3f}")
        
        # 生成相关性分析总结
        correlation_summary = generate_correlation_summary(correlation, p_value)
        logger.info(f"- 分析总结: {correlation_summary}")
        
        # 保存分析结果
        save_analysis_results(stock_code, merged_df, correlation, 
                            p_value < 0.05, correlation_summary, logger)
        
        # 可视化
        plot_correlation(merged_df, stock_code, correlation, logger)
        
    except Exception as e:
        logger.error(f"分析过程出错: {e}", exc_info=True)
    finally:
        engine.dispose()

def generate_correlation_summary(correlation, p_value):
    """生成相关性分析总结"""
    if p_value >= 0.05:
        return "情感变化与股价变动无显著相关性"
    
    strength = ""
    if abs(correlation) > 0.7:
        strength = "强"
    elif abs(correlation) > 0.4:
        strength = "中等"
    else:
        strength = "弱"
        
    direction = "正" if correlation > 0 else "负"
    
    return f"情感变化与股价变动呈{strength}度{direction}相关(相关系数:{correlation:.2f})"

def save_analysis_results(stock_code, analysis_df, correlation, is_significant, correlation_summary, logger):
    """保存分析结果到数据库"""
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks'
    }
    
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    
    try:
        # 删除旧数据
        with engine.begin() as conn:
            conn.execute(text(
                "DELETE FROM sentiment_price_correlation WHERE stock_code = :code"
            ), {'code': stock_code})
            logger.info(f"已删除股票{stock_code}的旧数据")
        
        records = []
        current_time = datetime.now()
        
        for _, row in analysis_df.iterrows():
            record = {
                'stock_code': stock_code,
                'date': row['date'],
                'sentiment_change': float(row['sentiment_change']) if not pd.isna(row['sentiment_change']) else 0,
                'price_change': float(row['price_change']) if not pd.isna(row['price_change']) else 0,
                'correlation': float(correlation),
                'sentiment_count': int(row['sentiment_count']),
                'is_significant': 1 if is_significant else 0,
                'correlation_summary': correlation_summary,
                'update_time': current_time
            }
            records.append(record)
        
        if records:
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO sentiment_price_correlation 
                    (stock_code, date, sentiment_change, price_change, 
                     correlation, sentiment_count, is_significant, correlation_summary, update_time)
                    VALUES 
                    (:stock_code, :date, :sentiment_change, :price_change,
                     :correlation, :sentiment_count, :is_significant, :correlation_summary, :update_time)
                """), records)
                logger.info(f"成功插入{len(records)}条记录")
                
    except Exception as e:
        logger.error(f"保存分析结果时出错: {e}", exc_info=True)
    finally:
        engine.dispose()

def plot_correlation(df, stock_code, correlation, logger):
    """绘制情感-股价关系图"""
    try:
        plt.figure(figsize=(10, 6))
        plt.scatter(df['sentiment_change'], df['price_change'], alpha=0.5)
        plt.xlabel('情感变化')
        plt.ylabel('股价变动(%)')
        plt.title(f'股票{stock_code}情感变化-股价变动关系图 (相关系数: {correlation:.3f})')
        
        # 添加趋势线
        z = np.polyfit(df['sentiment_change'], df['price_change'], 1)
        p = np.poly1d(z)
        plt.plot(df['sentiment_change'], p(df['sentiment_change']), "r--", alpha=0.8)
        
        # 保存图片
        save_dir = os.path.join(os.path.dirname(__file__), 'analysis_plots')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        plot_file = os.path.join(save_dir, f'{stock_code}_correlation.png')
        plt.savefig(plot_file)
        plt.close()
        
        logger.info(f"相关性图表已保存到: {plot_file}")
        
    except Exception as e:
        logger.error(f"绘制图表时出错: {e}", exc_info=True)

if __name__ == '__main__':
    # 设置日志
    logger = setup_logger()
    logger.info("开始运行情感-股价关系分析")
    
    try:
        # 创建数据表
        create_analysis_table()
        logger.info("数据表创建成功")
        
        # 获取所有股票代码
        stock_codes = get_stock_codes()
        if not stock_codes:
            logger.error("没有获取到股票代码")
            exit(1)
            
        logger.info(f"获取到{len(stock_codes)}个股票代码")
        
        # 分析每支股票
        for stock_code in stock_codes:
            logger.info(f"\n{'='*50}")
            logger.info(f"开始分析股票 {stock_code}")
            analyze_sentiment_price_relation(stock_code, logger)
            
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
    
    logger.info("分析完成") 