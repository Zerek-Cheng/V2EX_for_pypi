import json
import sys

import requests
from requests import Response


class ApiCli:
    __token: str
    __gate: str
    __debug: bool
    header = {}

    def __init__(self, token: str, gate="https://www.v2ex.com/api/v2/", debug: bool = False):
        """ 初始化API对象

        :param token: 在https://v2ex.com/settings/tokens申请到的token
        :param gate: RESTful API网关 默认为https://www.v2ex.com/api/v2/
        :param debug: 当debug为True时，所有的请求会直接print API接口请求结果

        Usage::
            >>>> import v2ex.v2ex
            >>>> api = v2ex.ApiCli(token="xxxxxxxx-xxxxxxxx-xxxxxxx-xxxxxxxx")
            >>>> api
        """

        self.__token = token
        self.__gate = gate
        self.__debug = debug

    def __request(self, path: str, params: dict[str, int | str | list | dict] | str = None, method="GET") -> requests:
        self.header["Authorization"] = "Bearer " + self.__token
        if method == "GET":
            return requests.request(
                url=self.__gate + path,
                params=params,
                method=method,
                headers=self.header,
            )
        elif method == "POST":
            return requests.request(
                url=self.__gate + path,
                data=params,
                method=method,
                headers=self.header,
            )

    def __json_to_dict(self, text: str) -> dict[str, object]:
        if self.__debug:
            print(text)
        return json.loads(text.encode("UTF8"))

    def notifications(self, page: int = 1):
        """ 获取最新的提醒

        :param page: 页码
        :return 由json解析而成的对象
        :rtype dict[str, object]

        Example Of return.result::

            List Of:
            {'id': 17452804, 'member_id': 90581, 'for_member_id': 578993, 'text': '<a
            href="/member/kennylam777"><strong>kennylam777</strong></a> 在 <a href="/t/860978#reply21">k8s 裸机配置时那么多的
            node、pod、service、PVC、PV 配置文件，都是硬记下来然后手写？还是说一般都是用到了去查？或者说普遍使用 GUI？还是说普遍不用裸机配置都是上云？</a> 里回复了你', 'payload': '基本上
            CKA 必考的題目，官方是用 kubectl - -dry-run', 'payload_rendered': '基本上 CKA 必考的題目，官方是用 kubectl - -dry-run', 'created':
            1656563191, 'member': {'username': 'kennylam777'}}

        """
        return self.__json_to_dict(self.__request(path=sys._getframe().f_code.co_name, params={"p": page}).text)

    def notifications_delete(self, noid: int) -> Response | None:
        """ 删除一个提醒
            Tip 截止到2022年6月30日23:56 该接口由于DELETE请求禁止暂时无法使用
                2022年7月1日09:30       接口不再报错，但无法使用

        :param noid: 提醒ID
        :return 此接口不同于其他接口使用的是DELETE方法，故直接返回requests对象结果，可能为None
        :rtype dict[str, object] | None

        Example Of return.result::

            List Of:
            ::TODO

        """
        return self.__request(path="notifications/" + str(noid), method="DELETE")

    def member(self) -> dict[str, object]:
        """ 获取自己的 Profile

        :return 由json解析而成的对象
        :rtype dict[str, object]

        Example Of return.result::
                {
              "success": true,
              "result": {
                "id": 578993,
                "username": "Zerek",
                "url": "https://www.v2ex.com/u/Zerek",
                "website": "",
                "twitter": null,
                "psn": null,
                "github": null,
                "btc": null,
                "location": "",
                "tagline": "",
                "bio": "",
                "avatar_mini": "https://cdn.v2ex.com/avatar/8352/b9e7/578993_mini.png?m=1650967416",
                "avatar_normal": "https://cdn.v2ex.com/avatar/8352/b9e7/578993_normal.png?m=1650967416",
                "avatar_large": "https://cdn.v2ex.com/avatar/8352/b9e7/578993_large.png?m=1650967416",
                "created": 1650602899,
                "last_modified": 1650967416
              }
            }
        """
        return self.__json_to_dict(
            self.__request(path=sys._getframe().f_code.co_name).text)

    def token(self) -> dict[str, object]:
        """ 查看当前使用的令牌

        :return 由json解析而成的对象
        :rtype dict[str, object]

        Example Of return.result::
            {
              "success": true,
              "message": "Current token details",
              "result": {
                "token": "your token",
                "scope": "everything",
                "expiration": 2592000,
                "good_for_days": 30,
                "total_used": 12,
                "last_used": 1656603303,
                "created": 1656599236
              }
            }
        """
        return self.__json_to_dict(
            self.__request(path=sys._getframe().f_code.co_name).text)

    def tokens(self, scope: str = "everything", expiration: int = 2592000) -> dict[str, object]:
        """ 创建新的令牌
            你可以在系统中最多创建 10 个 Personal Access Token。

        :param scope: 可选 everything 或者 regular，如果是 regular 类型的 Token 将不能用于进一步创建新的 token
        :param expiration: 可支持的值：2592000，5184000，7776000 或者 15552000，即 30 天，60 天，90 天或者 180 天的秒数

        :return 由json解析而成的对象
        :rtype dict[str, object]

        Example Of return.result::
            {
              "success": true,
              "result": {
                "token": "your new token"
              }
            }
        """
        return self.__json_to_dict(
            self.__request(path=sys._getframe().f_code.co_name, method="POST",
                           params=json.dumps({"scope": scope, "expiration": expiration})).text)

    def nodes(self, node_name: str = "python") -> dict[str, object]:
        """ 获取指定节点

        :param node_name: 节点name
        :return 由json解析而成的对象
        :rtype dict[str, object]

        Example Of return.result::

            {
              "success": true,
              "message": "Node details found",
              "result": {
                "id": 90,
                "url": "https://www.v2ex.com/go/python",
                "name": "python",
                "title": "Python",
                "header": "\u8fd9\u91cc\u8ba8\u8bba\u5404\u79cd Python \u8bed\u8a00\u7f16\u7a0b\u8bdd\u9898\uff0c\u4e5f\u5305\u62ec Django\uff0cTornado \u7b49\u6846\u67b6\u7684\u8ba8\u8bba\u3002\u8fd9\u91cc\u662f\u4e00\u4e2a\u80fd\u591f\u5e2e\u52a9\u4f60\u89e3\u51b3\u5b9e\u9645\u95ee\u9898\u7684\u5730\u65b9\u3002",
                "footer": "",
                "avatar": "https://cdn.v2ex.com/navatar/8613/985e/90_xxxlarge.png?m=1648339948",
                "topics": 15014,
                "created": 1278683336,
                "last_modified": 1648339948
              }
            }
        """
        return self.__json_to_dict(
            self.__request(path=sys._getframe().f_code.co_name + "/" + node_name).text)

    def nodes_topics(self, node_name: str = "python", p: int = 1) -> dict[str, object]:
        """ 获取指定节点下的主题

        :param node_name: 节点name
        :param p: 分页页码
        :return 由json解析而成的对象
        :rtype dict[str, object]

        Example Of return.result::
            List of:
                {
              "id": 863314,
              "title": "\u5bfb\u6c42\u5927\u4f6c\u5199\u4e00\u4e2a\u534f\u8bae\u6ce8\u518c apple id",
              "content": "\u5bfb\u6c42\u5927\u4f6c\u5199\u4e00\u4e2a\u534f\u8bae\u6ce8\u518c apple id \uff0c\u80fd\u529b\u6709\u9650\u53ea\u4f1a\u5199\u6a21\u62df\u7684\u3002\r\n1 \u3001\u53ef\u591a\u7ebf\u7a0b\u6279\u91cf\u6ce8\u518c\r\n2 \u3001\u652f\u6301\u4ee3\u7406\u6c60\r\n3 \u3001\u90ae\u7bb1\u9a8c\u8bc1\uff0c\u65e0\u9700\u624b\u673a\u53f7\uff08\u624b\u673a\u53f7\u9a8c\u8bc1\u4ee5\u540e\u9ed8\u8ba4\u5f00\u542f\u4e86\u4e24\u6b65\u8ba4\u8bc1\uff09\r\n\u5982\u6709\u610f\u8bf7\u7559\u8054\u7cfb\u65b9\u5f0f\uff0c\u611f\u8c22",
              "content_rendered": "<p>\u5bfb\u6c42\u5927\u4f6c\u5199\u4e00\u4e2a\u534f\u8bae\u6ce8\u518c apple id \uff0c\u80fd\u529b\u6709\u9650\u53ea\u4f1a\u5199\u6a21\u62df\u7684\u3002\n1 \u3001\u53ef\u591a\u7ebf\u7a0b\u6279\u91cf\u6ce8\u518c\n2 \u3001\u652f\u6301\u4ee3\u7406\u6c60\n3 \u3001\u90ae\u7bb1\u9a8c\u8bc1\uff0c\u65e0\u9700\u624b\u673a\u53f7\uff08\u624b\u673a\u53f7\u9a8c\u8bc1\u4ee5\u540e\u9ed8\u8ba4\u5f00\u542f\u4e86\u4e24\u6b65\u8ba4\u8bc1\uff09\n\u5982\u6709\u610f\u8bf7\u7559\u8054\u7cfb\u65b9\u5f0f\uff0c\u611f\u8c22</p>\n",
              "syntax": 1,
              "url": "https://www.v2ex.com/t/863314",
              "replies": 6,
              "last_reply_by": "realpg",
              "created": 1656600775,
              "last_modified": 1656600775,
              "last_touched": 1656473983
            },
        """
        return self.__json_to_dict(
            self.__request(path="nodes/" + node_name + "/topics",
                           params={"p": p}).text)

    def topics(self, topic_id: str = "1") -> dict[str, object]:
        """ 获取指定主题

        :param topic_id: 帖子ID

        :return 由json解析而成的对象
        :rtype dict[str, object]

        Example Of return.result::

            {
              "success": true,
              "message": "Topic details found",
              "result": {
                "id": 1,
                "title": "\u2665 Introducing Project Babel 2.0",
                "content": "xxxxx",
                "content_rendered": "xxxx",
                "syntax": 0,
                "url": "https://www.v2ex.com/t/1",
                "replies": 138,
                "last_reply_by": "villivateur",
                "created": 1272207387,
                "last_modified": 1495862399,
                "last_touched": 1617546331,
                "member": {
                  "id": 1,
                  "username": "Livid",
                  "bio": "",
                  "website": "",
                  "github": "V2EX",
                  "url": "https://www.v2ex.com/member/Livid",
                  "avatar": "https://cdn.v2ex.com/avatar/c4ca/4238/1_xxxlarge.png?m=1656456674",
                  "created": 1272203146
                },
                "node": {
                  "id": 1,
                  "url": "https://www.v2ex.com/go/babel",
                  "name": "babel",
                  "title": "Project Babel",
                  "header": "",
                  "footer": "",
                  "avatar": "https://cdn.v2ex.com/navatar/c4ca/4238/1_xxxlarge.png?m=1638536123",
                  "topics": 1123,
                  "created": 1272206882,
                  "last_modified": 1638536123
                },
                "supplements": []
              }
            }
        """
        return self.__json_to_dict(
            self.__request(path=sys._getframe().f_code.co_name + "/" + topic_id).text)

    def topics_replies(self, topic_id: str = "1", p: int = 1) -> dict[str, object]:
        """ 获取指定主题下的回复

        :param topic_id: 帖子ID
        :param p: 分页

        :return 由json解析而成的对象

        :rtype dict[str, object]

        Example Of return.result::
            List Of
            {
              "id": 26,
              "content": "\u6211\u89c9\u7684cloud\u90a3\u4e2a\u9879\u76ee\u6bd4\u8fd9\u4e2a\u66f4\u6709\u5b58\u5728\u4e0b\u53bb\u7684\u610f\u4e49",
              "content_rendered": "\u6211\u89c9\u7684cloud\u90a3\u4e2a\u9879\u76ee\u6bd4\u8fd9\u4e2a\u66f4\u6709\u5b58\u5728\u4e0b\u53bb\u7684\u610f\u4e49",
              "created": 1272219134,
              "member": {
                "id": 14,
                "username": "kissfire",
                "bio": "",
                "website": "",
                "github": "",
                "url": "https://www.v2ex.com/member/kissfire",
                "avatar": "https://cdn.v2ex.com/avatar/aab3/2389/14_large.png?m=1424454323",
                "created": 1272218970
              }
            },
        """
        return self.__json_to_dict(
            self.__request(path="topics/" + topic_id + "/replies", params={"p": p}).text)
