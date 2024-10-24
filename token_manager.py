import time
from farpush.tenant_access_token import get_tenant_access_token

class TokenManager:
    def __init__(self):
        self.token = None
        self.expiry_time = 0

    def get_token(self):
        if self.token is None or time.time() >= self.expiry_time:
            self.token, expire = get_tenant_access_token()
            if self.token:
                self.expiry_time = time.time() + expire - 60  # 提前60秒刷新
        return self.token

# 创建TokenManager的全局实例
token_manager = TokenManager()
