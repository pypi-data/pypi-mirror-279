# -*- coding: utf-8 -*-
import time
import uuid

from sparkproxy import config
from sparkproxy import http
from sparkproxy.rsa import to_string, to_hex


class SparkProxyClient(object):
    """资源管理客户端

    使用应用密钥生成资源管理客户端，可以进一步：
    1、部署服务和容器，获得信息
    2、创建网络资源，获得信息

    属性：
        auth: 应用密钥对，Auth对象
        host: API host

    接口：
        get_product_stock(args)
        create_proxy(args)
        renew_proxy(args)
        delete_proxy(stack)
        get_order(stack)
        get_instance(stack)
    """

    def __init__(self, auth, host=None):
        self.auth = auth
        if host is None:
            self.host = config.get_default("default_api_host")
        else:
            self.host = host

    def check_available(self):
        """测试接口是否正常

        验签成功后，把16进制字符串转为二进制、通过自己的私钥解密、把解密字符串用服务器的公钥加密，并转为16进制字符串

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回字符串
            - ResponseInfo    请求的Response信息
        """
        msg = "hello"
        encrypted_msg = self.auth.encrypt_using_remote_public_key(msg)
        ret, info = self.__post('CheckAvailable', encrypted_msg)
        if ret is not None and 'code' in ret and ret['code'] == 200:
            received_encrypted_msg = ret['data']
            try:
                received_decrypted_msg = self.auth.decrypt_using_private_key(received_encrypted_msg)
            except ValueError as e:
                raise ValueError("使用本地私钥解密失败")
            received_msg = to_string(received_decrypted_msg)
            return msg == received_msg, None

        return False, info

    def get_product_stock(self, proxy_type, country_code=None, area_code=None, city_code=None):
        """获取商品库存

        列出当前所有在售的商品及其库存信息。

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回服务组列表[<product1>, <product1>, ...]，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('GetProductStock',
                           {"proxyType": proxy_type, "countryCode": country_code, "areaCode": area_code, "cityCode": city_code})

    def get_product_stock2(self, proxy_type, country_code=None, area_code=None, city_code=None):
        """获取商品库存

        列出当前所有在售的商品及其库存信息。

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回服务组列表[<product1>, <product1>, ...]，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('GetProductStock',
                           {"proxyType": proxy_type, "countryCode": country_code, "areaCode": area_code, "cityCode": city_code},
                           version="2024-04-16")

    def create_proxy(self, req_order_no, sku, amount, duration, unit, country_code, area_code, city_code):
        """创建代理实例

        创建新代理实例，返回订单信息

        Args:
            - req_order_no: 请求方订单ID
            - sku:  商品ID
            - amount: IP数量
            - duration: 必要 时长 0无限制
            - unit: 单位 1 天;2 周（7天）;3 月(自然月; 4年(自然年365，366）
            - country_code: 必要,国家代码 3位 iso标准
            - area_code: 必要,州代码 3位 iso标准
            - city_code: 必要,城市代码 向我方提取

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('CreateProxy', {"reqOrderNo": req_order_no, "productId": sku, "amount": amount,
                                           "duration": duration, "unit": unit, "countryCode": country_code,
                                           "areaCode": area_code, "cityCode": city_code})

    def renew_proxy(self, req_order_no, instances):
        """续费代理实例

        续费新代理实例，返回新订单信息

        Args:
            - args:  订单&实例描述

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('RenewProxy', {"reqOrderNo": req_order_no, "instances": instances})
        if ret is not None and 'code' in ret and ret['code'] == 200:
            for ipInfo in ret['data']['ipInfo']:
                password = ipInfo["password"]
                if len(password) > 0:
                    ipInfo["password"] = self.auth.decrypt_using_private_key(password)
        return ret, info

    def delete_proxy(self, req_order_no, instances):
        """删除代理实例

        删除代理实例，删除即时生效

        Args:
            - args:  实例描述

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        return self.__post('DelProxy', {"reqOrderNo": req_order_no, "instanceIds": instances})

    def get_order(self, req_order_no):
        """获取订单信息

        获取订单信息

        Args:
            - req_order_no:  请求方订单ID

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetOrder', {"reqOrderNo": req_order_no})
        if ret is not None and 'code' in ret and ret['code'] == 200 and 'data' in ret:
            data = ret['data']
            if 'ipInfo' in data:
                for ipInfo in data['ipInfo']:
                    password = ipInfo["password"] if "password" in ipInfo else ''
                    if len(password) > 0:
                        ipInfo["password"] = self.auth.decrypt_using_private_key(password)
        return ret, info

    def get_instance(self, instance_id):
        """获取订单信息

        获取订单信息

        Args:
            - instance_id:  实例ID

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetInstance', {"instanceId": instance_id})
        if ret is not None and 'code' in ret and ret['code'] == 200 and 'data' in ret:
            data = ret['data']
            password = data["password"] if 'password' in data else ''
            if len(password) > 0:
                data["password"] = self.auth.decrypt_using_private_key(password)
        return ret, info

    def get_flow_balance(self, username):
        """获取订单信息

        获取订单信息

        Args:
            - username:  流量账号ID

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('GetFlowBalance', {"username": username})
        return ret, info

    def recharge_flow(self, username, req_order_no, flow, days):
        """流量充值

        Args:
            - username:  流量账号ID
            - req_order_no: 客方订单号
            - flow: 流量MB
            - days：有效期

        Returns:
            返回一个tuple对象，其格式为(<result>, <ResponseInfo>)
            - result          成功返回空dict{}，失败返回{"error": "<errMsg string>"}
            - ResponseInfo    请求的Response信息
        """
        ret, info = self.__post('RechargeFlow', {"username": username, "reqOrderNo": req_order_no, "flow": flow, "days": days})
        return ret, info

    def __request_params(self, method, version, args):
        base_params = {
            "method": method,
            "version": version if version is not None else "2024-04-08",
            "reqId": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "supplierNo": self.auth.get_supplier_no(),
            "sign": "",
            "params": args
        }
        base_params["sign"] = self.auth.token_of_request(base_params)
        return base_params

    def __post(self, method, data=None, version=None):
        url = '{0}/v1/open/api'.format(self.host)
        req = self.__request_params(method, version, data)
        return http._post(url, req)
