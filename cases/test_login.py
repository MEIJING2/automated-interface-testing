"""
测试登录页
method: POST
"""
# 正则表达式，用于字符串匹配
import re
# 测试框架
import pytest
#json schema验证器
from jsonschema.validators import validate
#自定义请求工具
from utils.request_util import Request
#yaml文件处理器
from utils.yaml_util import HandleYaml


#测试类装饰器，指定执行顺序为1
#数字小的先执行，数字大的后执行
@pytest.mark.order(1)
class TestLogin:
    # 登录页的接口
    url = 'login'

    # 注意: 正则表达式中不要写空格, 否则会报错
    pattern = '\S{120,}'

    # 定义接口返回响应的 json_schema
    # 校验json是否符合预期
    json_schema = {
        # 校验响应数据类型
        "type": "object",
        # data是可选的，code和msg为接口必返回的
        "required": ["code", "msg"],
        # 是否运行额外的字段
        # "additionalProperties": False,
        #定义字段类型
        "properties": {
            "code": {
                "type": "integer"
            },
            "msg": {
                "type": "string"
            },
            "data": {
                "type": ["string", "null", "object"]
            }
        }
    }
#参数化装饰器，下方为多个测试用例的传参数据,login参数名要保持一致
    @pytest.mark.parametrize("login", [
        {
            "username": "zhangsan",
            "password": "123459",
            "msg": "用户不存在/密码错误"
        },
        {
            "username": "lisi",
            "password": "admin12311",
            "msg": "登录用户：lisi 不存在"
        },
        {
            "username": "admin",
            "password": "adm222in123",
            "msg": "用户不存在/密码错误"
        },

    ])
    # login参数会自动接收每个测试数据
    def test_login_fail_post(self, login):
        # 1. 发起请求
        data = {
            "username": login["username"],#从参数获取用户名
            "password": login["password"],
        }
        #发起post请求
        # 注意 Request 这里要写上括号, 因为这是一个实例, 调用实例方法
        #json=data自动转为json
        r = Request().post(url=self.url, json=data)

        # 2. 验证响应结构
        validate(instance=r.json(), schema=self.json_schema)

        # 3. 校验响应结果
        assert r.json()["code"] == 500
        # assert r.json()["msg"] == login["msg"]
        #优化为关键字匹配
        assert login["msg"] in r.json()["msg"]

    # 登陆成功 - 正确的账号和密码
    # 测试登录成功, 不能只测试登录一个账户, 必须要测试登录多个账户, 这就需要用到参数化
    @pytest.mark.parametrize("login", [
        {
            "username": "admin",
            "password": "admin123"
        }
        # ,
        # {
        #     "username": "admin",
        #     "password": "admin123"
        # }
    ])
    def test_login_success_post(self, login):
        # 1. 发起请求
        data = {
            "username": login["username"],
            "password": login["password"]
        }

        r = Request().post(url=self.url, json=data)

        # 2. 校验返回的接口的字段类型是否正确
        validate(r.json(), self.json_schema)

        # 3. 校验返回的内容是否正确
        assert r.json()['code'] == 200
        assert r.json()['msg'] == '操作成功'

        token = r.json()["token"]
        # HandleYaml.write_yaml(filename='data.yml', data=token)
        HandleYaml.write_yaml('data.yml', {'User_token_header': token})


        # 4. 保存两个用户的登录凭证
        # token = None
        # if login["username"] == "admin":
        #     token = {
        #         "User_token_header1": r.json()["token"]
        #     }
        # else:
        #     token = {
        #         "User_token_header": r.json()["token"]
        #     }
        #
        # HandleYaml.write_yaml(filename='data.yml', data=token)
