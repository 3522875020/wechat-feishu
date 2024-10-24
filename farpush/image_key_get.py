import requests
from requests_toolbelt import MultipartEncoder
from itchat import get_head_img  # 确保从 itchat 导入 get_head_img
from itchat.config import OWNER_ID  # 从配置文件中获取群主ID
from token_manager import token_manager

def upload_image(image_path, image_type='avatar'):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    token = token_manager.get_token()
    
    if not token:
        print("无法获取有效的Token")
        return

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # 使用 requests_toolbelt 的 MultipartEncoder 构建请求体
    form = {
        'image_type': image_type,
        'image': (open(image_path, 'rb'))  # 读取图片文件
    }
    multi_form = MultipartEncoder(form)
    headers['Content-Type'] = multi_form.content_type

    response = requests.post(url, headers=headers, data=multi_form)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['code'] == 0:
            image_key = response_data['data']['image_key']
            print(f"图片上传成功，image_key: {image_key}")
            return image_key
        else:
            print(f"上传图片失败: {response_data['msg']}")
    else:
        print(f"HTTP请求失败: {response.status_code} {response.text}")

def get_and_upload_head_img(userName=None, chatroomUserName=None):
    # 获取头像
    head_img_path = 'head_img.jpg'  # 临时保存头像的路径
    get_head_img(userName=userName, chatroomUserName=chatroomUserName, picDir=head_img_path)

    # 上传头像
    image_key = upload_image(head_img_path, image_type='avatar')
    
    # 处理上传后的 image_key（如需要）
    if image_key:
        print(f"上传后的 image_key: {image_key}")
        return image_key  # 返回 image_key
    return None  # 如果上传失败，返回 None

if __name__ == "__main__":
    # 示例调用
    user_name_input = input("请输入用户名（或聊天室用户名）: ")
    image_key = get_and_upload_head_img(userName=user_name_input)  # 从外部传入用户名
    if image_key:
        print(f"获取到的 image_key: {image_key}")
    else:
        print("获取 image_key 失败")
