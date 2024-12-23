import requests
import time
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class XiangProxyPool:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.api_url = "https://api.xiaoxiangdaili.com/ip/get"
        self.current_proxy = None
        self.last_fetch_time = None
        
    def _fetch_proxy(self):
        """从API获取新的代理IP"""
        try:
            params = {
                'appKey': self.app_key,
                'appSecret': self.app_secret,
                'cnt': 1,
                'wt': 'json'
            }
            
            response = requests.get(self.api_url, params=params)
            data = response.json()
            
            if data['code'] != 200:
                logger.error(f"获取代理失败: {data['msg']}")
                return None
                
            proxy_info = data['data'][0]
            proxy = f"{proxy_info['ip']}:{proxy_info['port']}"
            logger.info(f"成功获取新代理: {proxy}")
            return proxy
            
        except Exception as e:
            logger.error(f"获取代理时发生错误: {e}")
            return None
            
    def get_proxy(self):
        """获取代理，遵守调用频率限制"""
        current_time = datetime.now()
        
        # 如果是首次获取或者距离上次获取超过10秒
        if (self.last_fetch_time is None or 
            (current_time - self.last_fetch_time).total_seconds() >= 10):
            
            new_proxy = self._fetch_proxy()
            if new_proxy:
                self.current_proxy = new_proxy
                self.last_fetch_time = current_time
                
        return {
            'http': f'http://{self.app_key}:{self.app_secret}@{self.current_proxy}',
            'https': f'http://{self.app_key}:{self.app_secret}@{self.current_proxy}'
        } if self.current_proxy else None
        
    def mark_failed(self):
        """标记当前代理失败"""
        current_time = datetime.now()
        
        # 如果距离上次获取超过10秒，则获取新代理
        if (self.last_fetch_time is None or 
            (current_time - self.last_fetch_time).total_seconds() >= 10):
            
            new_proxy = self._fetch_proxy()
            if new_proxy:
                self.current_proxy = new_proxy
                self.last_fetch_time = current_time
                return self.get_proxy()
        
        return None 