"""
用于操作 yaml 文件
"""
import yaml


class HandleYaml:
    # 装饰器，声明这是一个类方法，不需要创建实例就能调用
    # HandleYaml 类是工具类，不需要存储实例数据
    @classmethod
    # 将变量写入文件中，cls指向类
    def write_yaml(cls, filename, data):
        with open('./data/' + filename, 'a', encoding='utf8') as f:
            yaml.safe_dump(data=data, stream=f)

    @classmethod
    # 从文件中读取变量
    def read_yaml(cls, filename, key):
        with open('./data/' + filename, 'r', encoding='utf8') as f:
            content = yaml.safe_load(stream=f)
            return content[key]

    @classmethod
    # 清空文件
    def clear_yaml(cls, filename):
        with open('./data/' + filename, 'w', encoding='utf8') as f:
            f.truncate()