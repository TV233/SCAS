import requests
import time
# 应用账号（请替换为真实账号）
app_key = '1188405502527557632'
# 应用密码（请替换为真实密码）
app_secret = 'iqInXHaO'
api_url = "https://api.xiaoxiangdaili.com/ip/get"
def getProxy():
    res = requests.get(api_url, params={'appKey': app_key, 'appSecret': app_secret, 'wt': 'text', 'cnt': 1})
    content = str(res.content,'utf-8')
    print("API response: " + content)
    return content
def getUrlContent(url):
    p = getProxy()
    # 如需使用socks5代理，只需将下面http替换为socks5h即可
    proxyMeta = "http://%(user)s:%(pass)s@%(proxy)s" % {
        "proxy": p,
        "user": app_key,
        "pass": app_secret,
    }
    proxies = {
        'http': proxyMeta,
        'https': proxyMeta,
    }
    try:
        resp = requests.get(url=target_url, proxies=proxies)
    except Exception as e:
        print(e)
    else:
        print("Target response: " + resp.text)
target_url = "http://httpbin.org/ip"
for i in range(5):
    getUrlContent(target_url)
    time.sleep(10)