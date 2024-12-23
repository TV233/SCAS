import random
import re
import time
import requests
import csv
import os
from parsel import Selector
from colorama import Fore, init
from fake_useragent import UserAgent
from sqlalchemy import create_engine, text
from datetime import datetime
from itertools import cycle
from proxy_pool import XiangProxyPool
import pandas as pd

# 初始化Colorama用于输出着色
init()
base_url = 'https://guba.eastmoney.com'

# 确保data目录存在
data_dir = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 初始化代理池
proxy_pool = XiangProxyPool(
    app_key='1188405502527557632',
    app_secret='iqInXHaO'
)

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
    user_agent = get_random_user_agent()
    
    accepts = [
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    ]
    
    languages = [
        'zh-CN,zh;q=0.9,en;q=0.8',
        'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'en-US,en;q=0.9,zh-CN;q=0.8'
    ]
    
    return {
        'User-Agent': user_agent,
        'Accept': random.choice(accepts),
        'Accept-Language': random.choice(languages),
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Host': 'guba.eastmoney.com',
        'Referer': 'https://guba.eastmoney.com/',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }

def make_request(url, retries=3):
    """使用代理池发送请求"""
    for attempt in range(retries):
        try:
            print(Fore.BLACK + '-' * 50 + f' 正在获取：{url}')
            
            response = requests.get(
                url,
                headers=get_headers(),
                proxies=proxy_pool.get_proxy(),  # 使用当前代理，不重新获取
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

def crawl_content(stock_code, page=1):
    """ 获取指定页码的HTML内容 """
    url = f'{base_url}/list,{stock_code}_{page}.html' if page != 1 else f'{base_url}/list,{stock_code}.html'
    return make_request(url)
 
def spider_out_comment(content, stock_code):
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
        if id_value == stock_code:
            data.append({
                'title': item.css('div.title > a::text').get(),
                'update_time': item.xpath('.//div[contains(@class, "update")]/text()').get()
            })
    return data

def save_csv(data, stock_code, filename=None):
    """ 保存数据到CSV文件 """
    if not data:
        return False
        
    try:
        if filename is None:
            filename = os.path.join(data_dir, f'comments_{stock_code}.csv')
        
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

def get_stock_codes():
    """从数据库获取股票代码列表"""
    db_config = {
        'user': 'root',
        'password': '123456',
        'host': '127.0.0.1',
        'database': 'stocks'
    }
    
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT stock_code FROM stock_info"))
            return [row[0] for row in result]
    except Exception as e:
        print(Fore.RED + f"获取股票代码失败: {e}")
        return []
    finally:
        engine.dispose()

def check_existing_data(stock_code):
    """检查是否已有该股票的评论数据"""
    filename = os.path.join(data_dir, f'comments_{stock_code}.csv')
    if not os.path.exists(filename):
        return False, None
    
    try:
        df = pd.read_csv(filename)
        if len(df) < 10:  # 数据行数少于10行，需要重新爬取
            return False, None
        return True, filename
    except Exception as e:
        print(Fore.RED + f"检查现有数据时出错: {e}")
        return False, None

def check_date_cycle(data):
    """检查数据是否已经循环到一年前的日期"""
    if len(data) < 100:
        return False
        
    try:
        # 获取当前日期
        current_date = datetime.now().date()
        target_date = current_date.replace(year=current_date.year - 1)
        
        def parse_date(date_str):
            # 从日期字符串中提取月和日
            month, day = map(int, date_str.split()[0].split('-'))
            year = current_date.year
            
            # 构造完整日期
            date = datetime(year, month, day).date()
            
            # 如果日期在未来，说明应该是去年的日期
            if date > current_date:
                date = date.replace(year=year - 1)
                
            return date
        
        # 检查最后一条数据的日期
        last_date = parse_date(data[-1]['update_time'])
        
        # 打印调试信息
        print(Fore.BLUE + f"当前日期: {current_date}")
        print(Fore.BLUE + f"目标日期: {target_date}")
        print(Fore.BLUE + f"最后记录日期: {last_date}")
        
        # 如果最后一条记录的日期早于或等于目标日期，说明已经获取到足够的数据
        return last_date <= target_date
        
    except Exception as e:
        print(Fore.RED + f"检查日期循环时出错: {e}")
        print(Fore.RED + f"最后一行日期字符串: {data[-1]['update_time']}")
        return False

def crawl_stock_comments(stock_code):
    """爬取指定股票的评论"""
    print(Fore.GREEN + f'开始处理股票 {stock_code} 的评论数据...')
    
    # 检查是否已有数据
    has_data, filename = check_existing_data(stock_code)
    if has_data:
        print(Fore.GREEN + f'股票 {stock_code} 已有完整的评论数据，跳过爬取')
        return
    
    # 如果需要爬取，创建或清空文件
    filename = os.path.join(data_dir, f'comments_{stock_code}.csv')
    if os.path.exists(filename):
        os.remove(filename)
    
    empty_pages_count = 0
    current_page = 1
    all_data = []  # 用于存储所有爬取的数据
    
    while True:  # 移除max_pages限制
        # 获取新的代理IP
        proxies = proxy_pool.get_proxy()
        if not proxies:
            print(Fore.RED + "无法获取代理，等待重试...")
            time.sleep(10)
            continue
            
        print(Fore.BLUE + f'使用新代理: {proxies["http"]}')
        
        # 使用当前代理IP爬取页面
        pages_with_current_ip = 0
        proxy_failed = False
        
        while pages_with_current_ip < 30 and not proxy_failed:  # 每个代理最多爬30页
            try:
                content = crawl_content(stock_code, current_page)
                if content:
                    data = spider_out_comment(content, stock_code)
                    if data:
                        all_data.extend(data)
                        if save_csv(data, stock_code, filename):
                            empty_pages_count = 0
                            pages_with_current_ip += 1
                            current_page += 1
                            
                            # 检查是否已经获取到一年的数据
                            if check_date_cycle(all_data):
                                print(Fore.GREEN + f'股票 {stock_code} 已爬取完一年数据，停止爬取')
                                return
                            
                            # 每页之间短暂延时
                            time.sleep(random.uniform(0.2, 0.5))
                            continue
                    
                    empty_pages_count += 1
                    if empty_pages_count >= 5:
                        print(Fore.YELLOW + f'股票 {stock_code} 连续{empty_pages_count}页无数据，停止爬取')
                        return
                else:
                    proxy_failed = True
                    
            except Exception as e:
                print(Fore.RED + f'爬取错误: {e}')
                proxy_failed = True
                
            current_page += 1
        
        # 当前代理IP完成任务，根据实际爬取页数决定休息时间
        if pages_with_current_ip > 0:
            sleep_time = random.uniform(10, 15)  # 符合API的调用频率限制
            print(Fore.YELLOW + f'当前代理完成{pages_with_current_ip}页爬取，休息{sleep_time:.1f}秒...')
            time.sleep(sleep_time)
        else:
            # 如果当前代理一个页面都没爬成功，短暂休息后继续
            time.sleep(random.uniform(3, 5))

def distribute_crawl_tasks():
    """分布式爬取任务分配"""
    stock_codes = get_stock_codes()
    if not stock_codes:
        return
    
    # 将股票分成多组，每组一次爬取
    batch_size = 5  # 每批处理5个股票
    for i in range(0, len(stock_codes), batch_size):
        batch = stock_codes[i:i+batch_size]
        
        for stock_code in batch:
            crawl_stock_comments(stock_code)
        
        # 每组之间休息较短时间
        sleep_time = random.uniform(30, 60)  # 休息30-60秒
        print(Fore.YELLOW + f'当前批次完成，休息{sleep_time:.1f}秒...')
        time.sleep(sleep_time)

if __name__ == '__main__':
    try:
        distribute_crawl_tasks()
    except Exception as e:
        print(Fore.RED + f'程序执行错误: {e}')
    finally:
        print(Fore.GREEN + '程序执行完毕。')
