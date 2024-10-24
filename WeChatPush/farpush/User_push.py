import sqlite3
import itchat
from farpush.image_key_get import get_and_upload_head_img
from farpush.create_group import create_group
from token_manager import token_manager
import requests
import json

def initialize_database():
    db_file = 'database.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # 创建用户表，使用 NickName 作为唯一标识符
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NickName TEXT UNIQUE,
            chat_id TEXT NOT NULL,
            avatar TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# 在 main 函数或程序开始时调用初始化函数
initialize_database()
def get_chat_id_by_nickname(nick_name):
    db_file = 'database.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # 只使用 NickName 查询
    cursor.execute("SELECT chat_id FROM user_groups WHERE NickName = ?", (nick_name,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else None

def send_message(chat_id, message):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    token = token_manager.get_token()
    params = {"receive_id_type":"chat_id"}
    if not token:
        print("无法获取有效的Token")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    # 确保 content 是 JSON 字符串
    content = json.dumps({"text": message})  # 将内容转换为 JSON 字符串

    data = {
        "receive_id": chat_id,  # 确保使用正确的接收者 ID
        "receive_id_type": "chat_id",  # 确保使用正确的接收者 ID 类型
        "msg_type": "text",  # 指定消息类型
        "content": content  # 使用 JSON 字符串作为内容
    }

    # 记录发送的数据
    print("发送的数据:", json.dumps(data, ensure_ascii=False))  # 打印发送的数据以调试

    response = requests.post(url, params=params, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['code'] == 0:
            print("消息发送成功")
        else:
            print(f"发送消息失败: {response_data['msg']}")
    else:
        print(f"HTTP请求失败: {response.status_code} {response.text}")

def main(nick_name, user_name, message):
    chat_id = get_chat_id_by_nickname(nick_name)
    
    if chat_id is None:
        # 如果不存在 chat_id，获取头像并创建群组
        avatar = get_and_upload_head_img(userName=user_name)
        chat_id = create_group(nick_name, avatar, is_user=True)  # 添加 is_user=True
    
    if chat_id:
        send_message(chat_id, message)
    else:
        print("无法获取有效的 chat_id，无法发送消息。")

if __name__ == "__main__":
    initialize_database()  # 确保在任何数据库操作之前调用
    # 示例调用
    nick_name_input = input("请输入群组昵称: ")
    user_name_input = input("请输入用户名: ")
    message_input = input("请输入消息内容: ")  # 允许用户输入消息
    main(nick_name_input, user_name_input, message_input)  # 传递消息到 main
