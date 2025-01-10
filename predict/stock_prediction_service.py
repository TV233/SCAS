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
    
    def calculate_llm_confidence(self, predictions, recent_actual, sentiment_data=None):
        """计算LLM预测的置信度"""
        try:
            # 1. 计算预测准确度指标
            overlap_len = min(len(recent_actual), len(predictions))
            if overlap_len > 0:
                # 计算MSE和MAE
                mse = mean_squared_error(
                    recent_actual[:overlap_len],
                    predictions[:overlap_len]
                )
                mae = mean_absolute_error(
                    recent_actual[:overlap_len],
                    predictions[:overlap_len]
                )
                
                # 计算趋势准确度
                actual_trend = np.diff(recent_actual[:overlap_len].flatten())
                pred_trend = np.diff(predictions[:overlap_len].flatten())
                trend_accuracy = np.mean((np.sign(actual_trend) == np.sign(pred_trend)).astype(float))
                
                # 计算预测波动的合理性
                actual_volatility = np.std(recent_actual[:overlap_len])
                pred_volatility = np.std(predictions[:overlap_len])
                volatility_ratio = min(actual_volatility, pred_volatility) / max(actual_volatility, pred_volatility)
                
                # 综合多个指标计算置信度
                mse_confidence = 1 / (1 + mse)  # 0-1范围
                mae_confidence = 1 / (1 + mae)  # 0-1范围
                
                # 加权平均计算最终置信度
                confidence = (
                    0.3 * mse_confidence +  # MSE权重
                    0.3 * mae_confidence +  # MAE权重
                    0.2 * trend_accuracy +  # 趋势准确度权重
                    0.2 * volatility_ratio  # 波动合理性权重
                )
                
                return max(0.1, min(0.99, confidence))  # 确保置信度在0.1-0.99之间
            
            return 0.5  # 默认置信度
            
        except Exception as e:
            print(f"计算LLM置信度时出错: {e}")
            return 0.5

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
            if accuracy is not None:
                if model_name == "LLM":
                    # 使用改进的LLM置信度计算方法
                    recent_actual = self.close_prices[-90:]
                    confidence_level = self.calculate_llm_confidence(predictions, recent_actual)
                else:
                    # 其他模型使用R2分数,但需要处理负值
                    confidence_level = max(0.1, min(0.99, (accuracy + 1) / 2))  # 将R2转换到0.1-0.99范围
            else:
                confidence_level = 0.5  # 默认置信度
                
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
            # 获取K线数据
            kline_data = self.llm_service.get_kline_data(
                stock_code,
                start_date=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                end_date=datetime.now().strftime('%Y-%m-%d')
            )
            
            # 获取情感数据
            sentiment_data = self.llm_service.get_sentiment_data(stock_code)
            
            if kline_data is not None and sentiment_data is not None:
                # 使用异步运行LLM预测
                import asyncio
                llm_result = asyncio.run(
                    self.llm_service.predict_future(stock_code, kline_data, sentiment_data)
                )
                
                if llm_result is not None:
                    predictions, dates, analysis, factors = llm_result
                    llm_future = predictions.reshape(-1, 1)
                    
                    # 计算评估指标
                    # 使用最近90天的实际数据作为评估基准
                    recent_actual = self.close_prices[-90:]
                    if len(recent_actual) > 0:
                        # 只评估与实际数据重叠的部分
                        overlap_len = min(len(recent_actual), len(predictions))
                        llm_metrics = self.evaluate_model(
                            recent_actual[:overlap_len],
                            predictions[:overlap_len].reshape(-1, 1),
                            "LLM"
                        )
                        
                    print("\nLLM分析结果:")
                    print(f"分析: {analysis}")
                    print(f"影响因素: {factors}")
                    
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