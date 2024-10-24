from token_manager import token_manager

def some_function():
    token = token_manager.get_token()
    if token:
        print(f"使用Tenant Access Token: {token}")
    else:
        print("获取Tenant Access Token失败。")
