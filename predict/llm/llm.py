import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.preprocessing import MinMaxScaler
import logging
from datetime import datetime, timedelta
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input, Concatenate, Flatten
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import calendar

class LLMPredictionService:
    def __init__(self):
        """初始化服务"""
        self.setup_logger()
        self.setup_database()
        self.time_steps = 20  # 使用20天的数据作为一个预测窗口
        self.future_days = 90  # 预测未来90天
        self.scaler_price = MinMaxScaler(feature_range=(0, 1))
        self.scaler_sentiment = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        
    def setup_logger(self):
        """配置日志"""
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f'llm_prediction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def setup_database(self):
        """设置数据库连接"""
        db_config = {
            'user': 'root',
            'password': '123456',
            'host': '127.0.0.1',
            'database': 'stocks'
        }
        
        self.engine = create_engine(
            f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
        )
        
    def get_kline_data(self, stock_code, start_date=None, end_date=None):
        """从数据库获取K线数据"""
        try:
            query = """
                SELECT 
                    date_time,
                    open_price,
                    high_price,
                    low_price,
                    close_price,
                    volume,
                    trade_value
                FROM stock_kline 
                WHERE stock_code = :code
            """
            
            if start_date:
                query += " AND date_time >= :start_date"
            if end_date:
                query += " AND date_time <= :end_date"
                
            query += " ORDER BY date_time"
            
            params = {'code': stock_code}
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date
                
            df = pd.read_sql(text(query), self.engine, params=params)
            df['date_time'] = pd.to_datetime(df['date_time'])
            df.set_index('date_time', inplace=True)
            
            self.logger.info(f"成功获取股票{stock_code}的K线数据：{len(df)}条记录")
            return df
            
        except Exception as e:
            self.logger.error(f"获取K线数据时出错: {e}", exc_info=True)
            return None
            
    def get_sentiment_data(self, stock_code):
        """读取情感分析数据"""
        try:
            # 读取CSV文件
            sentiment_file = f'emotionRating_{stock_code}.csv'
            df = pd.read_csv(sentiment_file)
            
            # 转换时间格式
            def parse_date(date_str):
                """解析日期字符串，添加当前年份"""
                try:
                    # 提取月和日
                    month, rest = date_str.split('-')
                    day = rest.split()[0]
                    
                    # 获取当前年份
                    current_year = datetime.now().year - 1
                    
                    # 处理2月29日的情况
                    if month == '02' and day == '29':
                        if not calendar.isleap(current_year):
                            day = '28'  # 非闰年改为28日
                    
                    # 构建完整日期字符串
                    full_date_str = f"{current_year}-{month}-{day}"
                    return pd.to_datetime(full_date_str).date()  # 只保留日期部分
                    
                except Exception as e:
                    self.logger.warning(f"无法解析日期 {date_str}: {e}")
                    return None
            
            # 应用日期解析
            df['date'] = df['update_time'].apply(parse_date)
            
            # 过滤掉无效的日期
            df = df[df['date'].notna()]
            
            # 按日期聚合情感得分
            daily_sentiment = df.groupby('date').agg({
                'sentiment': ['mean', 'count']  # 计算平均情感分数和评论数量
            }).reset_index()
            
            daily_sentiment.columns = ['date', 'sentiment_mean', 'comment_count']
            daily_sentiment['date'] = pd.to_datetime(daily_sentiment['date'])
            daily_sentiment.set_index('date', inplace=True)
            
            # 打印一些统计信息
            self.logger.info(f"情感数据统计:")
            self.logger.info(f"总评论数: {len(df)}")
            self.logger.info(f"日期范围: {daily_sentiment.index.min()} 到 {daily_sentiment.index.max()}")
            self.logger.info(f"每日平均评论数: {daily_sentiment['comment_count'].mean():.2f}")
            
            return daily_sentiment
            
        except Exception as e:
            self.logger.error(f"读取情感数据时出错: {e}", exc_info=True)
            return None
            
    def align_and_prepare_data(self, stock_code, start_date=None, end_date=None):
        """对齐K线数据和情感数据，准备模型输入"""
        try:
            # 获取数据
            kline_data = self.get_kline_data(stock_code, start_date, end_date)
            sentiment_data = self.get_sentiment_data(stock_code)
            
            if kline_data is None or sentiment_data is None:
                return None, None
                
            # 打印数据范围信息
            self.logger.info(f"K线数据范围: {kline_data.index.min()} 到 {kline_data.index.max()}")
            self.logger.info(f"情感数据范围: {sentiment_data.index.min()} 到 {sentiment_data.index.max()}")
            
            # 确定共同的日期范围
            start_date = max(kline_data.index.min(), sentiment_data.index.min())
            end_date = min(kline_data.index.max(), sentiment_data.index.max())
            
            # 截取共同时间范围的数据
            kline_data = kline_data[start_date:end_date]
            sentiment_data = sentiment_data[start_date:end_date]
            
            # 对齐数据
            aligned_data = pd.merge(
                kline_data,
                sentiment_data,
                left_index=True,
                right_index=True,
                how='inner'
            )
            
            # 检查是否有足够的数据
            if len(aligned_data) < self.time_steps:
                self.logger.error(f"数据量不足: 只有{len(aligned_data)}条记录，需要至少{self.time_steps}条")
                return None, None
                
            # 处理缺失值
            if aligned_data.isnull().any().any():
                self.logger.warning("发现缺失值，使用前向填充方法处理")
                aligned_data = aligned_data.ffill()
            
            # 准备特征
            price_features = aligned_data[['close_price']].values
            sentiment_features = aligned_data[['sentiment_mean']].values
            
            # 数据归一化
            price_scaled = self.scaler_price.fit_transform(price_features)
            sentiment_scaled = self.scaler_sentiment.fit_transform(sentiment_features)
            
            # 创建时间序列数据
            X_price, X_sentiment, y = [], [], []
            
            for i in range(len(aligned_data) - self.time_steps):
                X_price.append(price_scaled[i:(i + self.time_steps)])
                X_sentiment.append(sentiment_scaled[i:(i + self.time_steps)])
                y.append(price_scaled[i + self.time_steps])
                
            X_price = np.array(X_price)
            X_sentiment = np.array(X_sentiment)
            y = np.array(y)
            
            self.logger.info(f"成功准备训练数据: {len(X_price)}组")
            return (X_price, X_sentiment, y), aligned_data
            
        except Exception as e:
            self.logger.error(f"准备数据时出错: {e}", exc_info=True)
            return None, None
            
    def build_model(self):
        """构建多模态融合模型"""
        try:
            # K线数据分支 - 使用LSTM
            price_input = Input(shape=(self.time_steps, 1), name='price_input')
            price_lstm = LSTM(50, return_sequences=True)(price_input)
            price_lstm = LSTM(50)(price_lstm)
            price_dense = Dense(25)(price_lstm)
            price_dropout = Dropout(0.2)(price_dense)
            
            # 情感数据分支 - 使用LSTM
            sentiment_input = Input(shape=(self.time_steps, 1), name='sentiment_input')
            sentiment_lstm = LSTM(50, return_sequences=True)(sentiment_input)
            sentiment_lstm = LSTM(50)(sentiment_lstm)
            sentiment_dense = Dense(25)(sentiment_lstm)
            sentiment_dropout = Dropout(0.2)(sentiment_dense)
            
            # 合并两个分支
            merged = Concatenate()([price_dropout, sentiment_dropout])
            
            # 输出层
            dense = Dense(50, activation='relu')(merged)
            dense = Dropout(0.2)(dense)
            output = Dense(1)(dense)
            
            # 创建模型
            model = Model(
                inputs=[price_input, sentiment_input],
                outputs=output
            )
            
            # 编译模型
            model.compile(
                optimizer=Adam(learning_rate=0.001),
                loss='mse',
                metrics=['mae']
            )
            
            self.model = model
            self.logger.info("成功构建多模态融合模型")
            return model
            
        except Exception as e:
            self.logger.error(f"构建模型时出错: {e}", exc_info=True)
            return None
            
    def train_model(self, X_price, X_sentiment, y, validation_split=0.2, epochs=50, batch_size=32):
        """训练模型"""
        try:
            if self.model is None:
                self.build_model()
                
            if self.model is None:
                return None
                
            # 分割训练集和验证集
            train_size = int(len(X_price) * (1 - validation_split))
            
            X_price_train = X_price[:train_size]
            X_price_val = X_price[train_size:]
            X_sentiment_train = X_sentiment[:train_size]
            X_sentiment_val = X_sentiment[train_size:]
            y_train = y[:train_size]
            y_val = y[train_size:]
            
            # 训练模型
            history = self.model.fit(
                [X_price_train, X_sentiment_train],
                y_train,
                validation_data=([X_price_val, X_sentiment_val], y_val),
                epochs=epochs,
                batch_size=batch_size,
                verbose=1
            )
            
            self.logger.info("模型训练完成")
            
            # 绘制训练历史
            self.plot_training_history(history)
            
            return history
            
        except Exception as e:
            self.logger.error(f"训练模型时出错: {e}", exc_info=True)
            return None
            
    def plot_training_history(self, history):
        """绘制训练历史"""
        try:
            plt.figure(figsize=(12, 4))
            
            # 绘制损失
            plt.subplot(1, 2, 1)
            plt.plot(history.history['loss'], label='训练损失')
            plt.plot(history.history['val_loss'], label='验证损失')
            plt.title('模型损失')
            plt.xlabel('Epoch')
            plt.ylabel('损失')
            plt.legend()
            
            # 绘制MAE
            plt.subplot(1, 2, 2)
            plt.plot(history.history['mae'], label='训练MAE')
            plt.plot(history.history['val_mae'], label='验证MAE')
            plt.title('平均绝对误差')
            plt.xlabel('Epoch')
            plt.ylabel('MAE')
            plt.legend()
            
            # 保存图片
            plot_dir = os.path.join(os.path.dirname(__file__), 'plots')
            if not os.path.exists(plot_dir):
                os.makedirs(plot_dir)
            
            plt.savefig(os.path.join(plot_dir, f'training_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'))
            plt.close()
            
        except Exception as e:
            self.logger.error(f"绘制训练历史时出错: {e}", exc_info=True)
            
    def predict_future(self, last_price_sequence, last_sentiment_sequence):
        """预测未来价格"""
        try:
            if self.model is None:
                self.logger.error("模型未训练")
                return None
                
            future_predictions = []
            current_price_seq = last_price_sequence.copy()
            current_sentiment_seq = last_sentiment_sequence.copy()
            
            for _ in range(self.future_days):
                # 预测下一天
                next_pred = self.model.predict(
                    [
                        current_price_seq.reshape(1, self.time_steps, 1),
                        current_sentiment_seq.reshape(1, self.time_steps, 1)
                    ],
                    verbose=0
                )
                
                future_predictions.append(next_pred[0, 0])
                
                # 更新序列
                current_price_seq = np.roll(current_price_seq, -1)
                current_price_seq[-1] = next_pred[0, 0]
                
                # 简单复制最后一天的情感数据
                current_sentiment_seq = np.roll(current_sentiment_seq, -1)
                current_sentiment_seq[-1] = current_sentiment_seq[-2]
                
            # 反归一化预测结果
            predictions_reshaped = np.array(future_predictions).reshape(-1, 1)
            return self.scaler_price.inverse_transform(predictions_reshaped)
            
        except Exception as e:
            self.logger.error(f"预测未来价格时出错: {e}", exc_info=True)
            return None
            
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'engine'):
            self.engine.dispose() 