from stock_prediction_service import StockPredictionService
import json

def main():
    # 初始化预测服务
    stock_code = '601360'
    service = StockPredictionService(f'cnn/{stock_code}_klines.csv')
    
    # 运行预测
    results = service.run_predictions(stock_code)
    
    # 打印结果
    print("\n预测结果:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # 比较模型性能
    metrics = results['metrics']
    best_model = min(metrics.items(), key=lambda x: x[1]['mse'])[0]
    print(f"\n最佳模型: {best_model}")

if __name__ == "__main__":
    main() 