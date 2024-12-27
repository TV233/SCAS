import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Table, MetaData, Column, String, Float, Date, DateTime, Integer, text
from datetime import datetime
import os
import matplotlib.pyplot as plt
from scipy import stats
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
        Column('sentiment_avg', Float),  # 当日平均情感值
        Column('price_change', Float),   # 当日股价变动百分比
        Column('next_day_price_change', Float),  # 次日股价变动百分比
        Column('correlation', Float),     # 情感与股价变动相关系数
        Column('sentiment_count', Integer),  # 情感评论数量
        Column('is_significant', Integer),   # 相关性是否显著(p值<0.05)
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
                open_price,
                close_price,
                high_price,
                low_price,
                volume,
                trade_value,
                amplitude,
                up_down_range,
                up_down_price,
                turnover_rate
            FROM stock_kline 
            WHERE stock_code = :code
            ORDER BY date_time
        """)
        
        df = pd.read_sql(query, engine, params={'code': stock_code})
        df['date'] = pd.to_datetime(df['date']).dt.date
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
        
        logger.info(f"每日情感统计:")
        logger.info(f"- 天数: {len(daily_sentiment)}")
        logger.info(f"- 平均情感值范围: {daily_sentiment['sentiment_avg'].min():.3f} - {daily_sentiment['sentiment_avg'].max():.3f}")
        
        # 计算股价变动百分比
        kline_df['price_change'] = kline_df['close_price'].pct_change() * 100
        kline_df['next_day_price_change'] = kline_df['price_change'].shift(-1)
        
        # 合并数据后，清理缺失值和异常值
        merged_df = pd.merge(daily_sentiment, kline_df[['date', 'price_change', 'next_day_price_change']], 
                            on='date', how='inner')
        
        # 删除任何包含NaN的行
        merged_df = merged_df.dropna(subset=['sentiment_avg', 'next_day_price_change'])
        
        # 移除异常值（使用3个标准差作为阈值）
        def remove_outliers(df, column):
            mean = df[column].mean()
            std = df[column].std()
            return df[abs(df[column] - mean) <= 3 * std]
        
        merged_df = remove_outliers(merged_df, 'next_day_price_change')
        merged_df = remove_outliers(merged_df, 'sentiment_avg')
        
        logger.info(f"清理后的数据:")
        logger.info(f"- 有效记录数: {len(merged_df)}")
        
        if len(merged_df) < 2:  # 确保至少有两个数据点
            logger.warning("数据点太少，无法进行相关性分析")
            return
            
        # 计算相关系数
        correlation = merged_df['sentiment_avg'].corr(merged_df['next_day_price_change'])
        
        # 计算显著性
        # 使用pearsonr替代linregress，因为它更适合相关性分析
        from scipy.stats import pearsonr
        correlation, p_value = pearsonr(merged_df['sentiment_avg'], 
                                      merged_df['next_day_price_change'])
        
        logger.info(f"相关性分析结果:")
        logger.info(f"- 相关系数: {correlation:.3f}")
        logger.info(f"- P值: {p_value:.3f}")
        logger.info(f"- 是否显著: {p_value < 0.05}")
        
        # 添加更详细的分析
        if p_value < 0.05:
            if correlation > 0:
                logger.info("结论: 情感与股价显著正相关")
            else:
                logger.info("结论: 情感与股价显著负相关")
        else:
            logger.info("结论: 情感与股价无显著相关性")
            
        # 添加滞后相关性分析
        for lag in [1, 2, 3, 5]:  # 分析不同的滞后天数
            lagged_df = merged_df.copy()
            lagged_df['next_day_price_change'] = lagged_df['next_day_price_change'].shift(-lag)
            lagged_df = lagged_df.dropna()
            
            if len(lagged_df) >= 2:
                lag_corr, lag_p = pearsonr(lagged_df['sentiment_avg'], 
                                         lagged_df['next_day_price_change'])
                logger.info(f"{lag}天滞后相关性: {lag_corr:.3f} (P值: {lag_p:.3f})")
        
        # 保存分析结果
        save_analysis_results(stock_code, merged_df, correlation, p_value < 0.05, logger)
        
        # 可视化
        plot_correlation(merged_df, stock_code, correlation, logger)
        
    except Exception as e:
        logger.error(f"分析过程出错: {e}", exc_info=True)
    finally:
        engine.dispose()

def save_analysis_results(stock_code, analysis_df, correlation, is_significant, logger):
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
        
        # 插入新数据
        current_time = datetime.now()
        records = []
        
        for _, row in analysis_df.iterrows():
            record = {
                'stock_code': stock_code,
                'date': row['date'],
                'sentiment_avg': float(row['sentiment_avg']),
                'price_change': float(row['price_change']) if not pd.isna(row['price_change']) else 0,
                'next_day_price_change': float(row['next_day_price_change']) if not pd.isna(row['next_day_price_change']) else 0,
                'correlation': float(correlation),
                'sentiment_count': int(row['sentiment_count']),
                'is_significant': 1 if is_significant else 0,
                'update_time': current_time
            }
            records.append(record)
        
        if records:
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO sentiment_price_correlation 
                    (stock_code, date, sentiment_avg, price_change, next_day_price_change, 
                     correlation, sentiment_count, is_significant, update_time)
                    VALUES 
                    (:stock_code, :date, :sentiment_avg, :price_change, :next_day_price_change,
                     :correlation, :sentiment_count, :is_significant, :update_time)
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
        plt.scatter(df['sentiment_avg'], df['next_day_price_change'], alpha=0.5)
        plt.xlabel('情感得分')
        plt.ylabel('次日股价变动(%)')
        plt.title(f'股票{stock_code}情感-股价关系图 (相关系数: {correlation:.3f})')
        
        # 添加趋势线
        z = np.polyfit(df['sentiment_avg'], df['next_day_price_change'], 1)
        p = np.poly1d(z)
        plt.plot(df['sentiment_avg'], p(df['sentiment_avg']), "r--", alpha=0.8)
        
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