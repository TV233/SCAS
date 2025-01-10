import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.preprocessing import MinMaxScaler
import logging
from datetime import datetime, timedelta
import os
import json
import aiohttp
import asyncio
import calendar

class LLMPredictionService:
    def __init__(self):
        """初始化服务"""
        self.setup_logger()
        self.setup_database()
        self.time_steps = 20  # 使用20天的数据作为预测窗口
        self.future_days = 90  # 预测未来90天
        self.scaler_price = MinMaxScaler(feature_range=(0, 1))
        self.scaler_sentiment = MinMaxScaler(feature_range=(0, 1))
        self.ollama_url = "http://localhost:11434/api/chat"
        
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
            sentiment_file = os.path.join(os.path.dirname(__file__), f'emotionRating_{stock_code}.csv')
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

    def prepare_prompt(self, kline_data, sentiment_data, stock_code):
        """准备提示词"""
        # 获取最近的K线数据
        recent_kline = kline_data.tail(self.time_steps)
        recent_sentiment = sentiment_data.tail(self.time_steps)
        
        # 构建提示词
        prompt = f"""你是一个专业的股票分析师和预测专家。请基于以下数据分析并预测股票 {stock_code} 未来90天(从{pd.Timestamp.now().strftime('%Y-%m-%d')}开始)的每日走势。

最近{self.time_steps}天的K线数据:
"""
        
        # 添加K线数据
        for date, row in recent_kline.iterrows():
            prompt += f"日期: {date.strftime('%Y-%m-%d')}, 开盘: {row['open_price']:.2f}, 收盘: {row['close_price']:.2f}, 最高: {row['high_price']:.2f}, 最低: {row['low_price']:.2f}, 成交量: {row['volume']}\n"
            
        prompt += "\n最近的市场情绪数据:\n"
        
        # 添加情感数据
        for date, row in recent_sentiment.iterrows():
            prompt += f"日期: {date.strftime('%Y-%m-%d')}, 情感得分: {row['sentiment_mean']:.2f}, 评论数: {row['comment_count']}\n"
            
        prompt += f"""
请仔细分析这些数据，并给出:
1. 未来90天(从{pd.Timestamp.now().strftime('%Y-%m-%d')}到{(pd.Timestamp.now() + pd.Timedelta(days=90)).strftime('%Y-%m-%d')})的每日收盘价预测
2. 每个预测的置信度(0-1之间)
3. 主要影响因素分析

注意:
- 必须预测完整的90天数据
- 每天都需要有具体的预测价格
- 预测应考虑历史趋势、市场情绪、技术指标等多个因素
- 预测结果应该反映真实的市场波动

请以JSON格式返回，格式如下:
{{
    "predictions": [
        {{"date": "YYYY-MM-DD", "price": float, "confidence": float}}
        // 需要90天的完整预测数据
    ],
    "analysis": "详细的分析文本",
    "factors": ["影响因素1", "影响因素2", "影响因素3"]
}}
"""
        return prompt

    async def predict_with_ollama(self, messages):
        """使用ollama进行预测"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.ollama_url,
                    json={
                        "model": "llama3.2",
                        "messages": messages,
                        "stream": False
                    },
                    headers={
                        'Content-Type': 'application/json'
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"Ollama API错误响应: {error_text}")
                        raise Exception(f"Ollama API返回错误: {response.status}")
                    
                    result = await response.json()
                    return result
                    
        except Exception as e:
            self.logger.error(f"调用Ollama API时出错: {e}", exc_info=True)
            return None

    def parse_prediction_response(self, response):
        """解析预测响应"""
        try:
            if not response or 'message' not in response:
                self.logger.error("无效的响应格式")
                return None
                
            content = response['message']['content']
            self.logger.debug(f"原始响应内容: {content}")
            
            # 提取JSON部分
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                self.logger.error("未找到JSON内容")
                return None
                
            json_str = content[start_idx:end_idx]
            
            # 预处理JSON字符串
            # 1. 移除可能的注释
            json_lines = json_str.split('\n')
            json_lines = [line for line in json_lines if not line.strip().startswith('//')]
            json_str = '\n'.join(json_lines)
            
            # 2. 确保日期格式正确
            import re
            json_str = re.sub(r'(\d{4}-\d{2}-\d{2})"', r'\1"', json_str)
            
            try:
                result = json.loads(json_str)
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON解析错误: {e}")
                self.logger.error(f"JSON内容: {json_str}")
                return None
            
            # 验证预测数据完整性
            if 'predictions' not in result or not result['predictions']:
                self.logger.error("预测数据为空")
                return None
                
            # 生成90天的预测数据
            start_date = pd.Timestamp.now()
            dates = []
            prices = []
            
            # 如果预测数据不足90天，使用最后一天的预测补齐
            last_price = None
            for i in range(self.future_days):
                target_date = start_date + pd.Timedelta(days=i+1)
                
                # 查找当天的预测
                price_found = False
                for pred in result['predictions']:
                    pred_date = pd.to_datetime(pred['date'])
                    if pred_date.date() == target_date.date():
                        prices.append(pred['price'])
                        dates.append(target_date)
                        last_price = pred['price']
                        price_found = True
                        break
                
                if not price_found and last_price is not None:
                    # 使用最后一个有效预测
                    prices.append(last_price)
                    dates.append(target_date)
            
            if len(prices) < self.future_days:
                self.logger.warning(f"预测数据不足90天，实际天数: {len(prices)}")
                if len(prices) == 0:
                    return None
                
                # 使用最后一个价格补齐到90天
                last_price = prices[-1]
                while len(prices) < self.future_days:
                    next_date = dates[-1] + pd.Timedelta(days=1)
                    prices.append(last_price)
                    dates.append(next_date)
            
            return np.array(prices), dates, result.get('analysis', ''), result.get('factors', [])
            
        except Exception as e:
            self.logger.error(f"解析预测响应时出错: {e}", exc_info=True)
            return None

    async def predict_future(self, stock_code, kline_data, sentiment_data):
        """预测未来价格"""
        try:
            # 准备提示词
            prompt = self.prepare_prompt(kline_data, sentiment_data, stock_code)
            
            # 构建消息
            messages = [
                {"role": "system", "content": "你是一个专业的股票分析师，精通技术分析和情感分析。"},
                {"role": "user", "content": prompt}
            ]
            
            # 调用ollama
            response = await self.predict_with_ollama(messages)
            if response is None:
                return None
                
            # 解析响应
            result = self.parse_prediction_response(response)
            if result is None:
                return None
                
            predictions, dates, analysis, factors = result
            
            self.logger.info("预测完成")
            self.logger.info(f"分析: {analysis}")
            self.logger.info(f"影响因素: {factors}")
            
            return predictions, dates, analysis, factors
            
        except Exception as e:
            self.logger.error(f"预测未来价格时出错: {e}", exc_info=True)
            return None

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'engine'):
            self.engine.dispose() 