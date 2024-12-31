from stock_prediction_service import StockPredictionService
import json
from sqlalchemy import create_engine, text
import pandas as pd
import os
import logging
from datetime import datetime

def setup_logger():
    """配置日志"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, f'prediction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def get_kline_data(logger):
    """从数据库获取601360的K线数据"""
    stock_code = '601360'
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks'
    }
    
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    
    try:
        query = text("""
            SELECT 
                date_time,
                open_price,
                high_price,
                low_price,
                close_price,
                volume,
                trade_value as amount
            FROM stock_kline 
            WHERE stock_code = '601360'
            ORDER BY date_time
        """)
        
        df = pd.read_sql(query, engine)
        
        # 保存为CSV文件供模型使用
        csv_path = 'cnn/601360_klines.csv'
        os.makedirs('cnn', exist_ok=True)
        df.to_csv(csv_path, index=False)
        
        logger.info(f"成功获取股票601360的K线数据：{len(df)}条记录")
        return csv_path
        
    except Exception as e:
        logger.error(f"获取K线数据时出错: {e}", exc_info=True)
        return None
    finally:
        engine.dispose()

def main():
    # 初始化日志
    logger = setup_logger()
    logger.info("开始运行股票预测程序")
    
    # 获取K线数据
    csv_path = get_kline_data(logger)
    
    if not csv_path:
        logger.error("无法获取K线数据，程序退出")
        return
        
    # 初始化预测服务并运行预测
    service = StockPredictionService(csv_path)
    results = service.run_predictions('601360')
    
    # 打印结果
    logger.info("\n预测结果:")
    logger.info(json.dumps(results, indent=2, ensure_ascii=False))
    
    # 比较模型性能
    metrics = results['metrics']
    best_model = min(metrics.items(), key=lambda x: x[1]['mse'])[0]
    logger.info(f"\n最佳模型: {best_model}")

if __name__ == "__main__":
    main() 