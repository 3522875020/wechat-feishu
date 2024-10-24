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
    
    # 创建群组表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatroom_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ChatRoomName TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            avatar TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Ensure this function is called before any database operations
initialize_database()

def get_chat_id_by_chatroomname(chatroom_name):
    db_file = 'database.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # 只使用群名称（NickName）来查询
    cursor.execute("SELECT chat_id FROM chatroom_groups WHERE ChatRoomName = ?", (chatroom_name,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else None

def send_message(chat_id, message):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    token = token_manager.get_token()
    params = {"receive_id_type": "chat_id"}
    
    if not token:
        print("无法获取有效的Token")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    content = json.dumps({"text": message})

    data = {
        "receive_id": chat_id,
        "receive_id_type": "chat_id",
        "msg_type": "text",
        "content": content
    }

    print("发送的数据:", json.dumps(data, ensure_ascii=False))

    response = requests.post(url, params=params, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['code'] == 0:
            print("消息发送成功")
        else:
            print(f"发送消息失败: {response_data['msg']}")
    else:
        print(f"HTTP请求失败: {response.status_code} {response.text}")

def main(chatroom_name, chatroom_id, message):
    chat_id = get_chat_id_by_chatroomname(chatroom_name)
    
    if chat_id is None:
        # 如果不存在 chat_id，获取群聊头像并创建飞书群组
        # 注意：这里仍然需要 chatroom_id 来获取头像
        avatar = get_and_upload_head_img(chatroomUserName=chatroom_id)
        chat_id = create_group(chatroom_name, avatar)  # 使用群名称创建群组
    
    if chat_id:
        send_message(chat_id, message)
    else:
        print("无法获取有效的 chat_id，无法发送消息。")

if __name__ == "__main__":
    # 示例调用
    chatroom_name_input = input("请输入微信群名称: ")
    chatroom_id_input = input("请输入微信群ID: ")
    message_input = input("请输入消息内容: ")
    main(chatroom_name_input, chatroom_id_input, message_input)
