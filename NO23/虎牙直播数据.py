import threading
import requests
import random

class Common:
    def __init__(self):
        pass

    def get_headers(self):
        uas = [
            "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
            "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",
            "Baiduspider-image+(+http://www.baidu.com/search/spider.htm)",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 YisouSpider/5.0 Safari/537.36",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Googlebot-Image/1.0; +http://www.google.com/bot.html)",
            "Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
            "Sogou News Spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
            "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Sosospider+(+http://help.soso.com/webspider.htm)",
            "Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)"
        ]
        ua = random.choice(uas)
        headers = {
            "user-agent": ua,
            "referer": "https://www.baidu.com"
        }
        return headers


def run(index, url, semaphore, headers):
    semaphore.acquire()  # 加锁
    res = requests.get(url, headers=headers, timeout=5)
    res.encoding = 'utf-8'
    text = res.text
    text = text.replace('getLiveListJsonpCallback(', '')
    text = text[:-1]
    # print(text)
    # json_data = json.loads(text)
    # print(json_data)
    save(index,text)
    semaphore.release()  # 释放


def save(index, text):
    with open(f"./虎牙/{index}.json", "w", encoding="utf-8") as f:
        f.write(f"{text}")
    print("该URL地址数据写入完毕")


if __name__ == '__main__':
    # 获取总页码
    first_url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&callback=&page=1'
    c = Common()
    res = requests.get(url=first_url, headers=c.get_headers())
    data = res.json()
    if data['status'] == 200:
        total_page = data['data']['totalPage']

    url_format = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&callback=getLiveListJsonpCallback&page={}'
    # 拼接URL，全局共享变量
    urls = [url_format.format(i) for i in range(1, total_page)]
    # 最多允许5个线程同时运行
    semaphore = threading.BoundedSemaphore(5)
    for i, url in enumerate(urls):
        t = threading.Thread(target=run, args=(i, url, semaphore, c.get_headers()))
        t.start()
    while threading.active_count() != 1:
        pass
    else:
        print('所有线程运行完毕')
