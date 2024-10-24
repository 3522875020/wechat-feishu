import json
import requests
import sqlite3
from itchat.config import OWNER_ID  # 从配置文件中获取群主ID
from token_manager import token_manager
from .image_key_get import get_and_upload_head_img

def create_group(name, avatar=None, is_user=False):
    # 如果没有传入avatar，则使用默认值
    if avatar is None:
        avatar = "default-avatar_44ae0ca3-e140-494b-956f-78091e348435"

    url = "https://open.feishu.cn/open-apis/im/v1/chats"
    token = token_manager.get_token()
    
    if not token:
        print("无法获取有效的Token")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    # 构建请求体
    data = {
        "name": name,
        "avatar": avatar,
        "owner_id": OWNER_ID,
        "description": "群描述",
        "i18n_names": {
            "zh_cn": name,
            "en_us": "group chat",
            "ja_jp": "グループチャット"
        },
        "group_message_type": "chat",
        "chat_mode": name,
        "chat_type": "private",
        "join_message_visibility": "all_members",
        "leave_message_visibility": "all_members",
        "membership_approval": "no_approval_required",
        "restricted_mode_setting": {
            "status": False,
            "screenshot_has_permission_setting": "all_members",
            "download_has_permission_setting": "all_members",
            "message_has_permission_setting": "all_members"
        },
        "urgent_setting": "all_members",
        "video_conference_setting": "all_members",
        "edit_permission": "all_members",
        "hide_member_count_setting": "all_members"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['code'] == 0:
            chat_id = response_data['data']['chat_id']
            print(f"群组创建成功，chat_id: {chat_id}")
            # 记录到SQLite数据库，传递 is_user 参数
            record_group_to_db(name, chat_id, avatar, is_user=is_user)
            return chat_id
        else:
            print(f"创建群组失败: {response_data['msg']}")
    else:
        print(f"HTTP请求失败: {response.status_code} {response.text}")

def record_group_to_db(name, chat_id, avatar, is_user=False):
    db_file = 'database.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    if is_user:
        # 用户表 - 使用 NickName 列名
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                NickName TEXT UNIQUE,
                chat_id TEXT,
                avatar TEXT
            )
        ''')
        
        cursor.execute(''' 
            INSERT OR REPLACE INTO user_groups (NickName, chat_id, avatar) 
            VALUES (?, ?, ?)
        ''', (name, chat_id, avatar))
    else:
        # 群组表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chatroom_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ChatRoomName TEXT UNIQUE,
                chat_id TEXT,
                avatar TEXT
            )
        ''')
        
        cursor.execute(''' 
            INSERT OR REPLACE INTO chatroom_groups (ChatRoomName, chat_id, avatar) 
            VALUES (?, ?, ?)
        ''', (name, chat_id, avatar))

    conn.commit()
    conn.close()
    print(f"群组信息已记录到数据库: {name}, {chat_id}, {avatar}")

if __name__ == "__main__":
    # 示例调用
    create_group("测试群名称")
