import random
import re
import time
import requests
import csv
import os
from parsel import Selector
from colorama import Fore, init
from fake_useragent import UserAgent
from datetime import datetime

# 初始化Colorama用于输出着色
init()
base_url = 'https://guba.eastmoney.com'
STOCK_CODE = '601360'  # 固定爬取601360

# 确保data目录存在
data_dir = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def get_random_user_agent():
    """随机获取用户代理"""
    try:
        ua = UserAgent()
        return ua.random
    except Exception as e:
        print(Fore.RED + f"Error creating UserAgent: {e}")
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

def get_headers():
    """构造请求头"""
    return {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Host': 'guba.eastmoney.com',
        'Referer': 'https://guba.eastmoney.com/'
    }

def make_request(url, retries=3):
    """发送请求"""
    for attempt in range(retries):
        try:
            print(Fore.BLACK + '-' * 50 + f' 正在获取：{url}')
            
            response = requests.get(
                url,
                headers=get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return response.text
            else:
                print(Fore.RED + f'获取页面失败，状态码: {response.status_code}')
                return None
                
        except requests.RequestException as e:
            print(Fore.RED + f'请求错误: {e}')
            if attempt < retries - 1:
                sleep_time = (attempt + 1) * 2
                print(Fore.YELLOW + f'等待{sleep_time}秒后重试...')
                time.sleep(sleep_time)
            
    return None

def crawl_content(page=1):
    """ 获取指定页码的HTML内容 """
    url = f'{base_url}/list,{STOCK_CODE}_{page}.html' if page != 1 else f'{base_url}/list,{STOCK_CODE}.html'
    return make_request(url)

def spider_out_comment(content):
    """ 解析HTML内容提取所需数据 """
    if not content:
        return []
        
    selector = Selector(text=content)
    list_body = selector.xpath('//li[contains(@class, "defaultlist")]/table[contains(@class, "default_list")]/tbody[contains(@class, "listbody")]/tr[contains(@class, "listitem")]')
    data = []
    
    for item in list_body:
        # 提取 id
        id_value = re.findall('[0-9]+', item.css('div.title > a').attrib['href'])[0]
        
        # 只保存与当前股票相关的评论
        if id_value == STOCK_CODE:
            data.append({
                'title': item.css('div.title > a::text').get(),
                'update_time': item.xpath('.//div[contains(@class, "update")]/text()').get()
            })
    return data

def save_csv(data, filename=None):
    """ 保存数据到CSV文件 """
    if not data:
        return False
        
    try:
        if filename is None:
            filename = os.path.join(data_dir, f'comments_{STOCK_CODE}.csv')
        
        # 指定列名
        fieldnames = ['title', 'update_time']
        
        # 检查文件是否存在，如果不存在则创建文件并写入表头
        write_header = not os.path.exists(filename)
        
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if write_header:
                writer.writeheader()
            
            writer.writerows(data)
            
        print(Fore.GREEN + f'成功保存{len(data)}条数据到CSV文件。')
        return True
    
    except Exception as e:
        print(Fore.RED + f'保存CSV文件失败: {e}')
        return False

def check_date_cycle(data):
    """检查数据是否已经循环到一年前的日期"""
    if len(data) < 100:
        return False
        
    try:
        current_date = datetime.now().date()
        target_date = current_date.replace(year=current_date.year - 1)
        
        def parse_date(date_str):
            month, day = map(int, date_str.split()[0].split('-'))
            year = current_date.year
            date = datetime(year, month, day).date()
            if date > current_date:
                date = date.replace(year=year - 1)
            return date
        
        last_date = parse_date(data[-1]['update_time'])
        
        print(Fore.BLUE + f"当前日期: {current_date}")
        print(Fore.BLUE + f"目标日期: {target_date}")
        print(Fore.BLUE + f"最后记录日期: {last_date}")
        
        return last_date <= target_date
        
    except Exception as e:
        print(Fore.RED + f"检查日期循环时出错: {e}")
        return False

def crawl_stock_comments():
    """爬取601360股票的评论"""
    print(Fore.GREEN + f'开始爬取股票 {STOCK_CODE} 的评论数据...')
    
    filename = os.path.join(data_dir, f'comments_{STOCK_CODE}.csv')
    # if os.path.exists(filename):
    #     os.remove(filename)
    
    empty_pages_count = 0
    current_page = 392
    all_data = []
    
    while True:
        try:
            content = crawl_content(current_page)
            if content:
                data = spider_out_comment(content)
                if data:
                    all_data.extend(data)
                    if save_csv(data, filename):
                        empty_pages_count = 0
                        
                        # 检查是否已经获取到一年的数据
                        if check_date_cycle(all_data):
                            print(Fore.GREEN + f'股票 {STOCK_CODE} 已爬取完一年数据，停止爬取')
                            return
                        
                        # 每页之间短暂延时
                        time.sleep(random.uniform(0.2, 0.3))
                        current_page += 1
                        continue
                
                empty_pages_count += 1
                if empty_pages_count >= 5:
                    print(Fore.YELLOW + f'股票 {STOCK_CODE} 连续{empty_pages_count}页无���据，停止爬取')
                    return
                    
        except Exception as e:
            print(Fore.RED + f'爬取错误: {e}')
            time.sleep(5)
            
        current_page += 1

if __name__ == '__main__':
    try:
        crawl_stock_comments()
    except Exception as e:
        print(Fore.RED + f'程序执行错误: {e}')
    finally:
        print(Fore.GREEN + '程序执行完毕。') 