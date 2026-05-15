"""
测试新增博客
url: http://www.029tec.com/prod-api/mes/md/workstation
method: POST
"""
import pytest
from jsonschema.validators import validate

from utils.request_util import Request
from utils.yaml_util import HandleYaml


@pytest.mark.order(3)
class TestAddBlog:
    # 新增的 url
    url = 'mes/md/unitmeasure'

    json_schema = {
        "type": "object",
        "required": ["code", "msg"],
        "properties": {
            "code": {
                "type": "integer"
            },
            "msg": {
                "type": ["string", "null"]
            }
        }
    }

    # 未登录状态下访问
    def test_add_not_login(self):
        # 1. 发起请求
        blog = {
            "measureCode": "10012",
            "measureName": "个",
            "primaryFlag": "Y",
            "changeRate": 0,
            "enableFlag": "N",
        }

        r = Request().post(url=self.url, data=blog)

        # 2. 判断接口返回响应的状态码
        assert r.json()['code'] == 401

    # 登录状态下访问 - POST
    # @pytest.mark.parametrize("blog", [
    #     {
    #         "measureCode": "100123",
    #         "measureName": "个",
    #         "primaryFlag": "Y",
    #         "changeRate": 0,
    #         "enableFlag": "N",
    #         "expected_code": 200,
    #         "msg": "操作成功"
    #     }
    # ])
    # def test_insert_login_post(self, blog):
    #     # 1. 获取token
    #     token = HandleYaml.read_yaml(filename='data.yml', key='User_token_header')
    #
    #     if not token:
    #         pytest.skip("未找到token，请先执行登录测试")
    #
    #     # 2. 设置请求头（添加Cookie！）
    #     headers = {
    #         'Accept': 'application/json, text/plain, */*',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Authorization': f'Bearer {token}',
    #         'Connection': 'keep-alive',
    #         'Content-Type': 'application/json;charset=UTF-8',
    #         'Origin': 'http://www.029tec.com',
    #         'Referer': 'http://www.029tec.com/mes/md/unitmeasure',  # 修改为正确的路径
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    #         # ✅ 添加 Cookie 到 headers 中
    #         'Cookie': f'sidebarStatus=1; Admin-Token={token}'
    #     }
    #
    #     print('header:', headers)
    #
    #     # 3. 准备请求数据
    #     data = {
    #         "measureCode": blog["measureCode"],
    #         "measureName": blog["measureName"],
    #         "primaryFlag": blog["primaryFlag"],
    #         "changeRate": blog["changeRate"],
    #         "enableFlag": blog["enableFlag"],
    #     }
    #
    #     print(f"请求数据: {data}")
    #
    #     # 4. 发起请求
    #     r = Request().post(url=self.url, headers=headers, json=data)
    #
    #     # 打印响应信息
    #     print(f"响应状态码: {r.status_code}")
    #     print(f"响应内容: {r.json()}")
    #
    #     # 5. 校验接口返回的字段数据格式是否正确
    #     validate(r.json(), self.json_schema)
    #
    #     # 6. 判断关键字段的值是否正确
    #     assert r.json()["code"] == blog["expected_code"]
    #     assert r.json()["msg"] == blog["msg"]  # 修复：应该是 == 而不是 in