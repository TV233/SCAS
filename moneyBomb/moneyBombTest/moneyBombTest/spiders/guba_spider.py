import scrapy
import pandas as pd
from scrapy.selector import Selector


class GubaSpider(scrapy.Spider):
    print("guba_spider")
    name = "guba_spider"
    start_urls = ['https://guba.eastmoney.com/list,601360.html']  # 初始URL

    def __init__(self, *args, **kwargs):
        super(GubaSpider, self).__init__(*args, **kwargs)
        self.data_frame = pd.DataFrame()  # 初始化一个空的DataFrame
        print("初始化爬虫")

    def parse(self, response):
        """解析股吧页面内容"""
        print(f"正在解析页面: {response.url}")

        # 解析股吧帖子内容
        selector = Selector(response)
        list_body = selector.xpath(
            '//li[contains(@class, "defaultlist")]/table[contains(@class, "default_list")]/tbody/tr[contains(@class, "listitem")]')

        # 如果页面没有解析到内容，打印提示
        if not list_body:
            print(f"未找到帖子内容: {response.url}")
        else:
            print(f"找到 {len(list_body)} 个帖子")

        # 存储每页解析的数据
        data = []
        for item in list_body:
            post_id = item.css('div.title > a::attr(href)').re_first(r'[0-9]+')
            if not post_id:
                print("未找到帖子ID，跳过该帖子")
                continue  # 跳过没有找到ID的帖子

            data.append({
                'id': post_id,
                'read_count': item.css('div.read::text').get(),
                'reply': item.css('div.reply::text').get(),
                'title': item.css('div.title > a::text').get(),
                'title_url': response.urljoin(item.css('div.title > a::attr(href)').get()),
                'author': item.css('div.author > a::text').get(),
                'author_url': response.urljoin(item.css('div.author > a::attr(href)').get()),
                'update_time': item.xpath('.//div[contains(@class, "update")]/text()').get(),
            })

        # 将数据添加到 DataFrame 中
        new_data = pd.DataFrame(data)
        self.data_frame = pd.concat([self.data_frame, new_data], ignore_index=True)

        # 打印解析到的帖子数和总数
        print(f"当前页面解析到 {len(data)} 条帖子")
        print(f"目前总共收集到 {len(self.data_frame)} 条帖子")

        # 获取下一页的链接并继续爬取
        next_page = selector.xpath('//a[@class="page-next"]/@href').get()
        if next_page:
            print(f"发现下一页链接: {next_page}")
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
        else:
            print("未找到下一页链接，爬虫结束")

            # 全部页面爬取结束后保存为CSV文件
            self.data_frame.to_csv('guba_data.csv', index=False, encoding='utf-8-sig')
            print("数据保存至 guba_data.csv 文件")
