# Sparkproxy OpenApi SDK for Python

[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/tag/sparkpoxy/spark-sdk-python.svg?label=release)](https://github.com/yungoo/spark-sdk-python/releases)
[![Latest Stable Version](https://img.shields.io/pypi/v/sparkproxy.svg)](https://pypi.python.org/pypi/sparkproxy)
[![Download Times](https://img.shields.io/pypi/dm/sparkproxy.svg)](https://pypi.python.org/pypi/sparkproxy)

## 安装

通过pip

```bash
$ pip install sparkproxy
```

## 运行环境

| sparkproxy SDK版本 |              Python 版本               |
|:----------------:| :------------------------------------: |
|      1.0.0       | 2.7, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9 |

## 使用方法

### 检查接口是否已经配置好

```python
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
with open("spark.pub", 'rb') as pem_file:
    rsa_public_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key, public_key=rsa_public_key), host=SANDBOX_API_HOST)

# 获取订单&实例信息
ret, info = client.check_available()
print(ret)
print(info)
```

### 调用sparkproxy的开放接口

```python
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST

# 双方协商的商户号
supplier_no = 'test0001'

# 使用私钥对请求签名（认证）, 生成方式参考 [examples示例](https://github.com/yungoo/spark-sdk-python/tree/master/examples/genrsa.py)。
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key), host=SANDBOX_API_HOST)

ret, info = client.get_product_stock(proxy_type=103)
if ret is not None:
    print('All is OK')
else:
    print(info) # error message in info
```

### 同步接口

参考 [examples示例](https://github.com/yungoo/spark-sdk-python/tree/master/examples/webhooks.py)。

```python
import os
from flask import Flask, request
from sparkproxy import Auth

# sparkproxy提供的公钥，用于验证同步接口的请求合法性
rsa_public_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEovKByCtmQlJJBsZzSyc97gI1
Dp62XP8SrvUPBqGlWGEKNh60n2njcUUIkMDitM2yb1vuRluu3Mzk/TvaE23JOMqA
0HPsd7IG9rNCyn7vcRXvVj1jLTVw/J+f7FJB4OzZqmOEe8kq69WCP4JIkXPvAT53
wvarJGl6cincWuZvIwIDAQAB
-----END PUBLIC KEY-----
'''

with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()

supplier_no = 'test0001'
auth = Auth(supplier_no=supplier_no, private_key=private_key, public_key=rsa_public_key)


def verify_request(req):
    if req.is_json:
        params = req.json

        try:
            auth.verify_callback(params['supplierNo'], params['sign'], params['timestamp'])
        except ValueError:
            return "Bad signature", 400
    else:
        return "Bad request", 400

    return None, 200


app = Flask(__name__)

@app.route("/checkAvailable", methods=["POST"])
def receiveCheckAvailable():
    # 验签
    ret, code = verify_request(request)
    if ret is not None:
        return ret, code

    # 取出参数字符串，把16进制字符串转为二进制
    cyper_text = request.json["data"]

    # 通过自己的私钥解密
    plain_text = auth.decrypt_using_private_key(cyper_text)

    # 把解密字符串用对方的公钥加密，并转为16进制字符串
    new_cyper_text = auth.encrypt_using_remote_public_key(plain_text)

    return {
        "code": 200,
        "msg": "ok",
        "data": new_cyper_text
    }

@app.route("/product/sync", methods=["POST"])
def receiveSyncProducts():
    ret, code = verify_request(request)
    if ret is not None:
        return ret, code

    return "", 200


@app.route("/instance/sync", methods=["POST"])
def receiveSyncInstances():
    ret, code = verify_request(request)
    if ret is not None:
        return ret, code

    ret = request.json
    if ret is not None and ret:
        for ipInfo in ret['data']['ipInfo']:
            password = ipInfo["password"]
            if len(password) > 0:
                ipInfo["password"] = auth.decrypt_using_private_key(password)

    print(ret)

    return "", 200


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
```


## 测试

``` bash
$ py.test
```


## 打包

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## 常见问题

- 第二个参数info保留了请求响应的信息，失败情况下ret 为none, 将info可以打印出来，提交给我们。
- API 的使用 demo 可以参考 [examples示例](https://github.com/yungoo/spark-sdk-python/tree/master/examples)。
- 如果碰到`ImportError: No module named requests.auth` 请安装 `requests` 。