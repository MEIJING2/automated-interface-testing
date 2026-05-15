"""
用于封装 request，requests 库专注于HTTP请求的发送
"""
import requests

from utils.logger_util import Logger


# 定义一个主机, 所有的 url 的主机都是相同的
# host = 'http://49.233.162.74:8080/'
host = 'http://www.029tec.com/prod-api/'


class Request:
    # 类属性，整个类共享
    # logger = Logger.getLogger()
    """
    定义初始化方法 - 用于获取日志对象
    类中的成员属性, 都可以放在初始化方法中进行初始化, 类似 java 中的构造方法, 完成成员属性的初始化
    """
    def __init__(self,need_auth=False):
        # 初始化日志对象
        # 每实例化一个 Request 对象, 都自带一个日志对象
        self.logger = Logger.getLogger()
        self.session = requests.Session()
        self.need_auth = need_auth

    '''
    用于调用 get 方法
    同时调用方法前后, 还可以封装打印日志的操作
    '''
    def get(self, url, **kwargs):
        # 1. 调用方法前, 打印日志
        self.logger.info('准备发起 get 请求, url: {}'.format(url))
        self.logger.info('接口信息: {}'.format(kwargs))

        # 2. 调用 get 方法
        r = requests.get(url=(host + url), **kwargs)

        # 3. 调用方法后, 打印日志
        self.logger.info('接口响应状态码: {}'.format(r.status_code))
        self.logger.info('接口响应内容: {}'.format(r.text))

        return r


    '''
    用于调用 post 方法
    同时调用方法前后, 还可以封装打印日志的操作
    '''
    def post(self, url, **kwargs):
        # 1. 调用方法前, 打印日志
        self.logger.info('准备开始发起 post 请求, url: {}'.format(url))
        self.logger.info('接口信息: {}'.format(kwargs))

        # 2. 调用 post 方法
        r = requests.post(url=(host + url), **kwargs)

        # 3. 调用方法后, 打印日志
        self.logger.info('接口响应状态码: {}'.format(r.status_code))
        self.logger.info('接口响应内容: {}'.format(r.text))

        return r





