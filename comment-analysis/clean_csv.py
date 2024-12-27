import pandas as pd
import os

def clean_sentiment_field():
    """去除CSV文件中的sentiment字段"""
    # 设置文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '')
    file_path = os.path.join(data_dir, 'emotionRating_601360.csv')
    
    try:
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 如果存在sentiment列，则删除
        if 'sentiment' in df.columns:
            df = df.drop('sentiment', axis=1)
            print("成功删除sentiment字段")
        else:
            print("文件中不存在sentiment字段")
        
        # 保存回原文件
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"文件已保存: {file_path}")
        
    except Exception as e:
        print(f"处理文件时出错: {e}")

if __name__ == '__main__':
    clean_sentiment_field() 