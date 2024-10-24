import json
import requests
from itchat.config import FEISHU_APP_ID, FEISHU_APP_SECRET

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            return data['tenant_access_token'], data['expire']
        else:
            print(f"Error: {data['msg']}")
    else:
        print(f"HTTP Error: {response.status_code}")

if __name__ == "__main__":
    token, expire = get_tenant_access_token()
    print(f"Tenant Access Token: {token}, Expire in: {expire} seconds")
