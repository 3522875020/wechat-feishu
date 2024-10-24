from pickle import NONE
import itchat
from itchat.content import TEXT, CARD, SHARING, PICTURE, EMOTICON, RECORDING, ATTACHMENT, WEBSHARE, SPLITTHEBILL, VIDEO, VOIP, FRIENDS, MUSICSHARE, LOCATIONSHARE, MAP, SERVICENOTIFICATION, RECALLED, MINIPROGRAM, CHATHISTORY, TRANSFER, REDENVELOPE, UNDEFINED, SYSTEMNOTIFICATION
from flask import Flask, request, jsonify, send_file  # type: ignore
import json
import _thread
from farpush.User_push import main as send_user_message  # Import the main function
from farpush.groups_push import main as send_group_message

app = Flask(__name__)

# 存储消息
messages = []

@app.route("/send", methods=['POST'])
def received():
    data = request.json
    username = data['username']
    content = data['content']
    itchat.send(content, toUserName=username)
    return 'ok'

@app.route("/getuser", methods=['POST'])
def getuser():
    data = request.json
    username = data['username']
    friends = itchat.search_friends(name=username)
    if friends:
        author = friends[0]
        user = {
            'nickName': author.nickName,
            'remarkName': author.remarkName,
            'headImage': author.get_head_image_url()
        }
        return json.dumps(user)
    return json.dumps({})

@app.route("/getmessagelist", methods=['GET'])
def getmessage():
    return json.dumps({"messages": messages})

@app.route("/getfile", methods=['POST'])
def getfile():
    filename = request.json['filename']
    return send_file(filename)
@itchat.msg_register([PICTURE, VIDEO, RECORDING, ATTACHMENT, WEBSHARE, MAP, EMOTICON])
def text_reply(msg):
    user_name = msg.get('FromUserName')
    nick_name = msg.get('User', {}).get('NickName', '') 
    text = ''  # Initialize text variable

    # Check the message type and set text accordingly
    if msg['Type'] == 'Picture':
        text = '[图片]'
    elif msg['Type'] == 'Video':
        text = '[视频]'
    elif msg['Type'] == 'Recording':
        text = '[语音]'
    elif msg['Type'] == 'Attachment':
        text = '[文件]'
    elif msg['Type'] == 'WebShare':
        text = '[分享]'
    elif msg['Type'] == 'Map':
        text = '[地图]'
    elif msg['Type'] == 'Emoticon':
        text = '[表情]'
# Debugging output to check the values
    print("Debug info:", {
        "user_name": user_name,
        "nick_name": nick_name,
        "text": text,
        "msg": msg
    })

    if user_name and nick_name and text:
        send_user_message(nick_name, user_name, text)  # Use nick_name as unique identifier
    else:
        print("缺少必要的字段，无法处理消息。")

@itchat.msg_register([VOIP])
def voip_reply(msg):
    print(msg)
    user_name = msg.get('FromUserName')
    nick_name = msg.get('User', {}).get('NickName', '')
    text = f'{nick_name}打来了语音通话'
    send_user_message(nick_name, user_name, text)

@itchat.msg_register([CHATHISTORY])
def chathistory_reply(msg):
    user_name = msg.get('FromUserName')
    nick_name = msg.get('User', {}).get('NickName', '')
    text = '[聊天记录]'
    send_user_message(nick_name, user_name, text)
@itchat.msg_register([TRANSFER])
def transfer_reply(msg):
    user_name = msg.get('FromUserName')
    nick_name = msg.get('User', {}).get('NickName', '')
    text = f"[转账] {msg.get('Content', '').split('<des><![CDATA[')[1].split(']]></des>')[0]}"
    send_user_message(nick_name, user_name, text)
@itchat.msg_register([REDENVELOPE])
def redenvelope_reply(msg):
    user_name = msg.get('FromUserName')
    nick_name = msg.get('User', {}).get('NickName', '')
    text = '[红包] 恭喜发财，大吉大利'
    send_user_message(nick_name, user_name, text)
@itchat.msg_register([TEXT,SYSTEMNOTIFICATION])
def text_reply(msg):
    # 提取所需的值
    user_name = msg.get('FromUserName')  # 用于获取头像
    nick_name = msg.get('User', {}).get('NickName', '')  # 用作唯一标识符
    text = msg.get('Content', '')  # 提取消息内容

    if user_name and nick_name and text:
        send_user_message(nick_name, user_name, text)  # 使用 nick_name 作为唯一标识符
    else:
        print("缺少必要的字段，无法处理消息。")

@itchat.msg_register([TEXT,SYSTEMNOTIFICATION,SPLITTHEBILL], isGroupChat=True)
def text_reply(msg):
    # 提取群聊消息所需的信息
    chatroom_name = msg['User'].get('NickName', '')  # 群聊名称
    chatroom_id = msg['FromUserName']  # 群聊ID
    actual_nickname = msg.get('ActualNickName', '')  # 发送者的昵称
    text = msg.get('Content', '')  # 消息内容
    
    # 组合发送者昵称和消息内容
    formatted_message = f"{actual_nickname}: {text}"
    
    if chatroom_name and chatroom_id and text:
        send_group_message(chatroom_name, chatroom_id, formatted_message)
    else:
        print("缺少必要的群聊信息，无法处理消息。")

@itchat.msg_register([PICTURE, VIDEO, RECORDING, ATTACHMENT, WEBSHARE, LOCATIONSHARE, MAP, EMOTICON], isGroupChat=True)
def group_text_reply(msg):
    # Extract necessary information from the group chat message
    chatroom_name = msg['User'].get('NickName', '')  # Group chat name
    chatroom_id = msg['FromUserName']  # Group chat ID
    actual_nickname = msg.get('ActualNickName', '')  # Sender's nickname
    text = ' ' # Message content
    if msg['Type'] == 'Picture':
        text = '[图片]'
    elif msg['Type'] == 'Video':
        text = '[视频]'
    elif msg['Type'] == 'Recording':
        text = '[语音]'
    elif msg['Type'] == 'Attachment':
        text = '[文件]'
    elif msg['Type'] == 'WebShare':
        text = '[分享]'
    elif msg['Type'] == 'Map':
        text = '[地图]'
    elif msg['Type'] == 'Emoticon':
        text = '[表情]'
    # Format the message to include the sender's nickname
    formatted_message = f"{actual_nickname}: {text}"

    if chatroom_name and chatroom_id and text:
        send_group_message(chatroom_name, chatroom_id, formatted_message)
    else:
        print("缺少必要的群聊信息，无法处理消息。")


@itchat.msg_register([CHATHISTORY], isGroupChat=True)
def group_chathistory_reply(msg):
    chatroom_name = msg['User'].get('NickName', '') 
    chatroom_id = msg['FromUserName']  # Group chat ID
    actual_nickname = msg.get('ActualNickName', '')
    formatted_message = f'{actual_nickname} [聊天记录]'
    
    if chatroom_id and formatted_message:
        send_group_message(chatroom_name, chatroom_id, formatted_message)
    else:
        print("缺少必要的字段，无法处理消息。")

@itchat.msg_register([TRANSFER], isGroupChat=True)
def group_transfer_reply(msg):
    chatroom_name = msg['User'].get('NickName', '') 
    chatroom_id = msg['FromUserName']  # Group chat ID
    formatted_message = f"[转账] {msg.get('Content', '').split('<des><![CDATA[')[1].split(']]></des>')[0]}"
    if chatroom_id and formatted_message:
        send_group_message(chatroom_name, chatroom_id, formatted_message)
    else:
        print("缺少必要的字段，无法处理消息。")
@itchat.msg_register([REDENVELOPE], isGroupChat=True)
def group_redenvelope_reply(msg):

    chatroom_name = msg['User'].get('NickName', '') 
    chatroom_id = msg['FromUserName']  # Group chat ID
    formatted_message = ' [红包] 恭喜发财，大吉大利'
    
    if chatroom_id and formatted_message:
        send_group_message(chatroom_name, chatroom_id, formatted_message)
    else:
        print("缺少必要的字段，无法处理消息。")

def flask(ip, port):
    from waitress import serve
    serve(app, host=ip, port=port)

if __name__ == '__main__':
    _thread.start_new_thread(flask, ('0.0.0.0', 9091))
    itchat.auto_login(hotReload=True, enableCmdQR=2)  # Set enableCmdQR to 2 to print QR code in terminal
    itchat.run()
