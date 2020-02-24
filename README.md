# ProxyPool

## 安装

### 安装Python

至少Python3.5以上

### 安装Redis

安装好之后将Redis服务开启

### 配置代理池

```
cd proxypool
```

#### 打开代理池和API

```
python3 run.py
```

## 获取代理


利用requests获取方法如下

```
import requests

PROXY_POOL_URL = 'http://localhost:5000/get'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
```

[https://github.com/Python3WebSpider/ProxyPool]
