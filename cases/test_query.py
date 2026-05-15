"""
测试博客列表页
url: http://www.029tec.com/prod-api/mes/md/workstation/list?pageNum=1&pageSize=10&workstationName=hhh
method: GET
"""
import pytest
from jsonschema.validators import validate

from utils.request_util import Request
from utils.yaml_util import HandleYaml


@pytest.mark.order(2)
class TestGetWorkstationList:
    # 接口的 url
    url = 'mes/md/workstation/list'

    # 接口返回数据的数据类型
    json_schema = {
        "type": "object",
        "required": ["code", "msg", "rows"],
        "properties": {
            "code": {
                "type": "integer"
            },
            "msg": {
                "type": "string"
            },
            "rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["workstationCode", "workstationName", "workstationAddress", "processName",
                                 "enableFlag"],
                    "additionalProperties": True,
                    "properties": {
                        "workstationCode": {"type": "string"},
                        "workstationName": {"type": "string"},
                        "workstationAddress": {"type": "string"},
                        "processName": {"type": "string"},
                        "enableFlag": {"type": "string"}
                    }
                }
            }
        }
    }

    # 验证未登录的场景
    @pytest.mark.parametrize("query", [
        {
            "pageNum": 1,
            "pageSize": 10,
            "workstationName": "hhh",
        }
    ])
    def test_list_not_login(self, query):
        # 请求体参数
        params = {
            "pageNum": query["pageNum"],
            "pageSize": query["pageSize"],
            "workstationName": query["workstationName"],
        }
        # 检查Request类是否添加了headers
        req = Request()
        print(f"请求头: {req.session.headers}")

        # 发起请求
        r = Request().get(url=self.url, params=params)
        # 打印响应信息
        print(f"响应状态码: {r.status_code}")
        print(f"响应头: {dict(r.headers)}")
        print(f"响应内容: {r.json()}")

        # 1. HTTP层面：请求成功到达服务器
        assert r.status_code == 200, f"HTTP状态码应该是200，实际={r.status_code}"

        # 2. 业务层面：认证失败
        response_data = r.json()
        assert response_data['code'] == 401, f"业务状态码应该是401，实际={response_data['code']}"
        assert "认证失败" in response_data['msg'], "认证失败消息不正确"

    # ✅ 验证登录的场景 - 注意正确的缩进
    @pytest.mark.parametrize("query", [
        {
            "pageNum": 1,
            "pageSize": 10,
            "workstationName": "hhh",
        }
    ])
    def test_list_login_get(self, query):
        print('执行登录后查询')
        # 1. 获取token，设置请求头
        token = HandleYaml.read_yaml(filename='data.yml', key='User_token_header')

        # 如果token不存在，跳过测试
        if not token:
            pytest.skip("未找到token，请先执行登录测试")

        header = {"Authorization": f"Bearer {token}"}

        # 请求体参数
        params = {
            "pageNum": query["pageNum"],
            "pageSize": query["pageSize"],
            "workstationName": query["workstationName"],
        }

        # 发起请求
        r = Request().get(url=self.url, params=params, headers=header)

        # 2. 校验返回的接口的字段类型是否正确
        validate(r.json(), self.json_schema)

        # 3. 校验返回的内容是否正确
        assert r.json()['code'] == 200
        assert r.json()["msg"] == "查询成功"