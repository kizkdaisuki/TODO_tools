from global_vars import GB_URL
import requests


class User:
    def __init__(self, username: str, password: str):
        # TODO 这里应该是从缓存中获取uid，如果缓存中没有，则请求接口获取
        self.my_username = username
        self.my_password = password
        self.uid = 0
        self.my_em
        # TODO 如果用户名不存在，则注册
        self.method_select()

    def method_select(self):
        # TODO 自动选择登录还是注册
        # TODO 查看 requests 的返回值
        # TODO not exists 则创建新的用户

        pass

    def method_login(self):
        # TODO 检查缓存是否可用，如果可以那就不需要重新请求
        pass

    def method_register(self):
        # TODO 注册功能
        pass

    def method_get_user_info(self):
        # TODO 获取用户的信息
        pass

    def method_bind_bilibili_uid(self):
        # TODO 绑定bilibili的uid
        pass

    def method_clock_in(self):
        # TODO 打卡

        pass

    def method_start_task(self):
        # TODO 开始任务

        pass

    def method_end_task(self):
        # TODO 结束任务

        pass

    def method_get_ranklist(self):
        # TODO 获取排行榜

        pass
