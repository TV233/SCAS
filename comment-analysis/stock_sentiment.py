from snownlp import SnowNLP, sentiment
import jieba
import re

class StockSentiment:
    def __init__(self):
        # 加载股票特定的情感词典
        self.stock_sentiment_dict = {
            # 积极词
            '利好': 1.5,
            '涨停': 2.0,
            '增长': 1.2,
            '上涨': 1.2,
            '突破': 1.3,
            '反弹': 1.0,
            '拉升': 1.2,
            '牛市': 1.5,
            '底部': 1.0,
            '机会': 1.0,
            '潜力': 1.0,
            '强势': 1.2,
            
            # 消极词
            '利空': -1.5,
            '跌停': -2.0,
            '下跌': -1.2,
            '跳水': -1.3,
            '破位': -1.2,
            '亏损': -1.5,
            '套牢': -1.3,
            '垃圾': -1.5,
            '割肉': -1.3,
            '崩盘': -1.8,
            '见底': -1.0,
            '弱势': -1.2
        }
        
        # 加载自定义训练的模型
        sentiment.load('stock_sentiment.marshal')
        
        # 添加最小评论长度限制
        self.min_length = 2
    
    def clean_text(self, text):
        """清理文本"""
        if not isinstance(text, str):
            return ""
            
        # 移除特殊字符但保留中文
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)
        return text
    
    def is_valid_comment(self, text):
        """检查评论是否有效"""
        if not text:
            return False
        if len(text) < self.min_length:
            return False
        # 检查是否只包含标点符号或特殊字符
        if not re.search(r'[\u4e00-\u9fa5a-zA-Z0-9]', text):
            return False
        return True
    
    def extract_features(self, text):
        """提取特征"""
        features = {
            'has_number': bool(re.search(r'\d+', text)),  # 是否包含数字
            'length': len(text),  # 评论长度
            'sentiment_words': sum(1 for word in jieba.cut(text) if word in self.stock_sentiment_dict)  # 情感词数量
        }
        return features
    
    def analyze(self, text):
        """分析评论情感"""
        try:
            # 清理文本
            cleaned_text = self.clean_text(text)
            
            # 检查评论是否有效
            if not self.is_valid_comment(cleaned_text):
                return 0.5  # 对于无效评论返回中性分数
            
            # 基础情感分数
            try:
                base_score = SnowNLP(cleaned_text).sentiments
            except:
                # 如果 SnowNLP 分析失败，使用词典进行简单分析
                base_score = 0.5
            
            # 提取特征
            features = self.extract_features(cleaned_text)
            
            # 根据特定词典调整分数
            adjustment = 0
            words = list(jieba.cut(cleaned_text))
            
            # 如果评论太短且没有情感词，返回中性分数
            if len(words) < 2 and not any(word in self.stock_sentiment_dict for word in words):
                return 0.5
                
            for word in words:
                if word in self.stock_sentiment_dict:
                    adjustment += self.stock_sentiment_dict[word]
            
            # 结合基础分数和调整值
            final_score = max(0, min(1, base_score + adjustment * 0.1))
            
            # 根据特征微调
            if features['has_number'] and base_score > 0.5:
                final_score *= 1.1  # 包含数字的正面评论可能更可信
            final_score = min(1.0, final_score)  # 确保不超过1.0
            
            return final_score
            
        except Exception as e:
            print(f"分析评论出错: {text}, 错误: {e}")
            return 0.5  # 发生错误时返回中性分数 