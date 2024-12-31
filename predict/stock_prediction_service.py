import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D, Flatten
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Table, MetaData, insert, text
from datetime import datetime, timedelta
from llm.llm import LLMPredictionService  # 导入LLM服务

class StockPredictionService:
    def __init__(self, data_path):
        # 加载数据
        self.data = pd.read_csv(data_path)
        
        # 适配新的字段名称
        if 'close_price' in self.data.columns:
            self.close_prices = self.data['close_price'].values.reshape(-1, 1)
        else:
            self.close_prices = self.data['close'].values.reshape(-1, 1)
        
        # 初始化 scaler
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = self.scaler.fit_transform(self.close_prices)
        
        # 设置时间步长和预测天数
        self.time_steps = 20
        self.future_days = 90
        
        # 数据库配置
        self.db_config = {
            'user': 'root',
            'password': '123456',
            'host': '127.0.0.1',
            'database': 'stocks'
        }
        
        # 创建数据库连接
        self.engine = create_engine(
            f"mysql+mysqlconnector://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}/{self.db_config['database']}"
        )
        
        # 初始化LLM服务
        self.llm_service = LLMPredictionService()

            
    def prepare_data(self, data, time_steps):
        X, y = [], []
        for i in range(len(data) - time_steps):
            X.append(data[i:(i + time_steps)])
            y.append(data[i + time_steps])
        return np.array(X), np.array(y)
    
    def build_cnn_model(self):
        model = Sequential([
            Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(self.time_steps, 1)),
            MaxPooling1D(pool_size=2),
            Conv1D(filters=32, kernel_size=3, activation='relu'),
            MaxPooling1D(pool_size=2),
            Flatten(),
            Dense(50, activation='relu'),
            Dropout(0.2),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def build_lstm_model(self):
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(self.time_steps, 1)),
            LSTM(50),
            Dense(25),
            Dropout(0.2),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def evaluate_model(self, y_true, y_pred, model_name):
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        print(f"\n{model_name} 评估结果:")
        print(f"均方误差 (MSE): {mse:.4f}")
        print(f"平均绝对误差 (MAE): {mae:.4f}")
        print(f"R2 分数: {r2:.4f}")
        
        return {'mse': mse, 'mae': mae, 'r2': r2}
    
    def predict_future(self, model, last_sequence):
        """预测未来90天的股价"""
        future_predictions = []
        current_sequence = last_sequence.copy()
        
        for _ in range(self.future_days):
            # 预测下一天
            next_pred = model.predict(current_sequence.reshape(1, self.time_steps, 1))
            future_predictions.append(next_pred[0, 0])
            
            # 更新序列，移除最早的一天，添加新预测的一天
            current_sequence = np.roll(current_sequence, -1)
            current_sequence[-1] = next_pred
            
        # 反归一化预测结果
        return self.scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
    
    def save_predictions_to_db(self, predictions, model_name, stock_code, accuracy=None):
        """保存预测结果到数据库"""
        metadata = MetaData()
        predictions_table = Table('predictions', metadata, autoload_with=self.engine)
        
        with self.engine.begin() as connection:
            # 删除该股票该模型的旧预测数据
            connection.execute(
                text("DELETE FROM predictions WHERE stock_code = :code AND model_name = :model"),
                {"code": stock_code, "model": model_name}
            )
            
            # 计算置信度
            confidence_level = accuracy if accuracy else 0.5
            
            # 插入新的预测数据
            for i, price in enumerate(predictions):
                prediction_date = pd.Timestamp.now() + pd.Timedelta(days=i+1)
                stmt = insert(predictions_table).values(
                    stock_code=stock_code,
                    model_name=model_name,
                    prediction_date=prediction_date.date(),
                    predicted_price=float(price[0]),
                    accuracy=accuracy,
                    confidence_level=confidence_level,
                    created_at=pd.Timestamp.now()
                )
                connection.execute(stmt)
    
    def run_predictions(self, stock_code):
        """运行所有预测模型"""
        # 运行CNN和LSTM预测
        X, y = self.prepare_data(self.scaled_data, self.time_steps)
        split = int(len(X) * 0.8)
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        # 训练和评估 CNN 模型
        cnn_model = self.build_cnn_model()
        cnn_model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
        cnn_pred = cnn_model.predict(X_test)
        cnn_metrics = self.evaluate_model(y_test, cnn_pred, "CNN")
        
        # 训练和评估 LSTM 模型
        lstm_model = self.build_lstm_model()
        lstm_model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
        lstm_pred = lstm_model.predict(X_test)
        lstm_metrics = self.evaluate_model(y_test, lstm_pred, "LSTM")
        
        # 获取最后的序列用于预测未来
        last_sequence = self.scaled_data[-self.time_steps:]
        
        # 预测未来90天
        cnn_future = self.predict_future(cnn_model, last_sequence)
        lstm_future = self.predict_future(lstm_model, last_sequence)
        
        # 运行LLM预测
        llm_future = None
        llm_metrics = {'mse': None, 'mae': None, 'r2': None}
        try:
            # 准备LLM数据
            data_tuple, _ = self.llm_service.align_and_prepare_data(
                stock_code,
                start_date=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                end_date=datetime.now().strftime('%Y-%m-%d')
            )
            
            if data_tuple is not None:
                X_price, X_sentiment, y = data_tuple
                
                # 训练LLM模型
                history = self.llm_service.train_model(X_price, X_sentiment, y)
                
                if history is not None:
                    # 准备预测数据
                    last_price_sequence = X_price[-1]
                    last_sentiment_sequence = X_sentiment[-1]
                    
                    # 预测未来90天
                    llm_future = self.llm_service.predict_future(
                        last_price_sequence,
                        last_sentiment_sequence
                    )
                    
                    # 计算LLM模型的评估指标
                    llm_pred = self.llm_service.model.predict(
                        [X_price[-len(X_test):], X_sentiment[-len(X_test):]]
                    )
                    llm_metrics = self.evaluate_model(y[-len(X_test):], llm_pred, "LLM")
        except Exception as e:
            print(f"LLM预测出错: {e}")
        
        # 保存预测结果到数据库
        self.save_predictions_to_db(cnn_future, "CNN", stock_code, cnn_metrics['r2'])
        self.save_predictions_to_db(lstm_future, "LSTM", stock_code, lstm_metrics['r2'])
        if llm_future is not None:
            self.save_predictions_to_db(llm_future, "LLM", stock_code, llm_metrics['r2'])
        
        return {
            'metrics': {
                'cnn': cnn_metrics,
                'lstm': lstm_metrics,
                'llm': llm_metrics
            },
            'predictions': {
                'cnn': cnn_future.tolist(),
                'lstm': lstm_future.tolist(),
                'llm': llm_future.tolist() if llm_future is not None else None
            }
        }
        
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'engine'):
            self.engine.dispose() 