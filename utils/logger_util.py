"""
用于封装日志功能
"""
import logging
import os.path
import time


'''
定义一个 info 级别的日志过滤器
继承 logging.Filter 类
'''
class InfoLogFilter(logging.Filter):
    # 定义过滤方法 - 类似 java 中方法的重写
    def filter(self, record):
        return record.levelno == logging.INFO


'''
定义一个 error 级别的日志过滤器
继承 logging.Filter 类
'''
class ErrorLogFilter(logging.Filter):
    # 定义过滤方法 -  类似 java 中的方法重写
    def filter(self, record):
        return record.levelno == logging.ERROR


class Logger:

    # 用于打印日志
    # 打印日志不需要每次都创建新的对象, 使用一个类对象即可, 因此定义一个类似 java/c++ 静态方法的方法
    @classmethod
    def getLogger(cls):
        # 1. 定义一个日志对象，name 是当前模块的名称，可以区分不同模块的日志
        cls.logger = logging.getLogger(__name__)
        # 2. 设置日志对象打印的日志级别
        # 日志从低到高级别分为 DEBUG，INFO，WARNING，ERROR，CRITICAL，高于设定级别的日志才会被记录
        cls.logger.setLevel(logging.DEBUG)

        # 3. 判断是否存在 logs 目录
        log_path = './logs'
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        # 4. 设定一级目录 - 文件名使用日期进行命名, 例如: 2025-12-19.log
        now = time.strftime('%Y-%m-%d')
        #    定义三种文件
        #    第一种存所有的 log
        log = log_path + '/' + now + '.log'
        #    第二种存 info 级别的 log
        info_log = log_path + '/' + now + '_info.log'
        #    第三种存 error 级别的 log
        err_log = log_path + '/' + now + '_err.log'

        # 5. 定义日志处理器 - 文件处理器, 传入日志文件的路径和名称
        #    注意: 需要写入中文日志, 因此要指定文件的编码方式为 utf8
        handler = logging.FileHandler(log, encoding='utf8')
        info_log_handler = logging.FileHandler(info_log, encoding='utf8')
        err_log_handler = logging.FileHandler(err_log, encoding='utf8')

        # 6. 设置日志的格式
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d)] - %(message)s'
        )

        # 7. 将日志的样式添加到日志处理器
        handler.setFormatter(formatter)
        info_log_handler.setFormatter(formatter)
        err_log_handler.setFormatter(formatter)

        # 8. 日志处理器添加过滤条件
        info_log_handler.addFilter(InfoLogFilter())
        err_log_handler.addFilter(ErrorLogFilter())

        # 9. 将日志处理器添加到日志对象
        cls.logger.addHandler(handler)
        cls.logger.addHandler(info_log_handler)
        cls.logger.addHandler(err_log_handler)

        return cls.logger






