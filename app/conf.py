__author__ = 'house'

ALERTS = [
    {
        'url': 'http://182.93.50.250:5000/rss.html',
        'alert_receiver': ['house@sietai.com']
    },
    # {
    #     'url': 'http://vastcm.com:5000/rss.html',
    #     'alert_receiver': ['yangyihao@live.cn', 'imdeveloper@163.com']
    # }
]

MONITOR_INTERVAL = 6   # seconds

RETRY_TIMES_FOR_DOWN = 2    # retry times for confirming server is down


