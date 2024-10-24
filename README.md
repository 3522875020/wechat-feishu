## 使用方法

1. 运行应用程序：

    ```bash
    python main.py
    ```
2. 登录飞书开放平台!
3. [image](assets/image-20241024171059-tcp69fu.png)
4. 创建企业自建应用!
   [image](assets/image-20241024171221-eonchgq.png)
5. 进入权限管理开通aily:message:write

    contact:user.employee:readonly
    contact:user.employee_id:readonly
    contact:user.id:readonly
    event:ip_list
    im:chat
    im:chat:create
    im:message
    im:message:send_as_bot
    im:resource
6.   手机上审核通过
    ![image](assets/image-20241024171545-sy2duf6.png)
7. 进入![image](assets/image-20241024171901-7gpbsbd.png)
    复制App ID与App Secre，
8. 点击https://open.feishu.cn/api-explorer/

    ![image](assets/image-20241024172157-lsvmeud.png)
    选择成员中选择自己复制
9. 将所有参数填入itchat\config.py中
10. 运行应用程序：

    ```bash
       python main.py
    ```
11. 当提示时，使用微信应用扫描终端中显示的二维码以登录。
