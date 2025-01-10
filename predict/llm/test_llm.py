import pandas as pd
import numpy as np
from llm import LLMPredictionService
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import asyncio

async def test_model():
    # 初始化服务
    service = LLMPredictionService()
    
    # 设置股票代码和时间范围
    stock_code = '601360'
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 使用最近一年的数据
    
    # 获取数据
    kline_data = service.get_kline_data(
        stock_code,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )
    
    sentiment_data = service.get_sentiment_data(stock_code)
    
    if kline_data is None or sentiment_data is None:
        print("数据获取失败")
        return
        
    # 预测未来价格
    result = await service.predict_future(stock_code, kline_data, sentiment_data)
    
    if result is None:
        print("预测失败")
        return
        
    predictions, dates, analysis, factors = result
    
    # 可视化预测结果
    plot_predictions(kline_data, predictions, dates, analysis, factors)
    
def plot_predictions(kline_data, predictions, pred_dates, analysis, factors):
    """可视化历史数据和预测结果"""
    try:
        plt.figure(figsize=(15, 8))
        
        # 创建两个子图
        ax1 = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2)
        
        # 绘制历史价格和预测价格
        ax1.plot(kline_data.index, kline_data['close_price'], 
                label='历史价格', color='blue')
        ax1.plot(pred_dates, predictions, 
                label='预测价格', color='red', linestyle='--')
        
        ax1.set_title('股票价格预测')
        ax1.set_xlabel('日期')
        ax1.set_ylabel('价格')
        ax1.legend()
        ax1.grid(True)
        
        # 添加分析文本
        ax2.axis('off')
        analysis_text = f"分析结果:\n{analysis}\n\n主要影响因素:\n"
        for i, factor in enumerate(factors, 1):
            analysis_text += f"{i}. {factor}\n"
        ax2.text(0, 0.5, analysis_text, fontsize=10, verticalalignment='center')
        
        plt.tight_layout()
        
        # 保存图片
        plt.savefig(f'plots/prediction_result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        plt.close()
        
        # 打印预测结果
        print("\n预测结果:")
        for date, price in zip(pred_dates, predictions):
            print(f"{date.strftime('%Y-%m-%d')}: {price:.2f}")
            
    except Exception as e:
        print(f"绘制预测结果时出错: {e}")

if __name__ == "__main__":
    asyncio.run(test_model()) 