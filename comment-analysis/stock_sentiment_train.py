import pandas as pd
from snownlp import sentiment
import os

def prepare_training_data():
    """准备股票领域特定的训练数据"""
    
    # 读取标注数据集
    data_path = os.path.join(os.path.dirname(__file__), '中文股票评论文本数据集.csv')
    df = pd.read_csv(data_path)
    
    # 分离正面和负面评论
    pos_comments = df[df['label'] == 1]['sentence'].tolist()
    neg_comments = df[df['label'] == 0]['sentence'].tolist()
    
    print(f"正面评论数量: {len(pos_comments)}")
    print(f"负面评论数量: {len(neg_comments)}")
    
    # 保存训练数据
    data_dir = os.path.join(os.path.dirname(__file__), 'training_data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    with open(os.path.join(data_dir, 'pos.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(pos_comments))
        
    with open(os.path.join(data_dir, 'neg.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(neg_comments))
        
    print("训练数据准备完成")

def train_model():
    """训练特定领域的情感分析模型"""
    data_dir = os.path.join(os.path.dirname(__file__), 'training_data')
    
    # 使用特定领域的数据训练模型
    sentiment.train(
        os.path.join(data_dir, 'neg.txt'),
        os.path.join(data_dir, 'pos.txt')
    )
    
    # 保存模型
    sentiment.save('stock_sentiment.marshal')
    print("模型训练完成")

def test_model():
    """测试模型效果"""
    # 读取原始数据集
    data_path = os.path.join(os.path.dirname(__file__), '中文股票评论文本数据集.csv')
    df = pd.read_csv(data_path)
    
    # 随机选择10条评论进行测试
    test_samples = df.sample(n=10)
    
    # 加载训练好的模型
    from stock_sentiment import StockSentiment
    analyzer = StockSentiment()
    
    print("\n测试结果:")
    print("-" * 50)
    for _, row in test_samples.iterrows():
        score = analyzer.analyze(row['sentence'])
        predicted = 1 if score > 0.5 else 0
        print(f"评论: {row['sentence']}")
        print(f"实际标签: {row['label']}")
        print(f"预测标签: {predicted} (情感得分: {score:.3f})")
        print("-" * 50)

if __name__ == '__main__':
    prepare_training_data()
    train_model()
    test_model() 