import requests

from . import storage

class Core(object):
    def __init__(self):
        ''' init 是 core.py 中唯一定义的方法
            alive 是一个值，表示核心是否正在运行
                - 你应该调用 logout 方法来改变它
                - 登出后，核心对象可以再次登录
            storageClass 仅使用基本的 Python 类型
                - 所以对于高级用法，请自行继承
            receivingRetryCount 是接收循环重试的次数
                - 现在是 5，但实际上即使 1 也足够
                - 失败就是失败
        '''
        self.alive, self.isLogging = False, False
        self.storageClass = storage.Storage(self)
        self.memberList = self.storageClass.memberList
        self.mpList = self.storageClass.mpList
        self.chatroomList = self.storageClass.chatroomList
        self.msgList = self.storageClass.msgList
        self.loginInfo = {}
        self.s = requests.Session()
        self.uuid = None
        self.functionDict = {'FriendChat': {}, 'GroupChat': {}, 'MpChat': {}}
        self.useHotReload, self.hotReloadDir = False, 'itchat.pkl'
        self.receivingRetryCount = 5
    def login(self, enableCmdQR=False, picDir=None, qrCallback=None,
            loginCallback=None, exitCallback=None):
        ''' 像网页微信一样登录
            登录时
                - 将下载并打开一个二维码
                - 然后记录扫描状态，暂停以供你确认
                - 最后登录并显示你的昵称
            选项
                - enableCmdQR: 在命令行中显示二维码
                    - 整数可以用于适应奇怪的字符长度
                - picDir: 存储二维码的地方
                - qrCallback: 应接受 uuid、状态、二维码的方法
                - loginCallback: 成功登录后的回调
                    - 如果未设置，屏幕将被清除，二维码将被删除
                - exitCallback: 登出后的回调
                    - 包含调用 logout
            用法
                ..code::python

                    import itchat
                    itchat.login()

            它定义在 components/login.py 中
            当然，登录中的每一个动作都可以在外部调用
                - 你可以扫描源代码以查看如何
                - 并根据自己的需求进行修改
        '''
        raise NotImplementedError()
    def get_QRuuid(self):
        ''' 获取二维码的 uuid
            uuid 是二维码的标识
                - 登录时，你需要先获取 uuid
                - 下载二维码时，你需要将 uuid 传递给它
                - 检查登录状态时，uuid 也是必需的
            如果 uuid 超时，只需获取另一个
            它定义在 components/login.py 中
        '''
        raise NotImplementedError()
    def get_QR(self, uuid=None, enableCmdQR=False, picDir=None, qrCallback=None):
        ''' 下载并显示二维码
            选项
                - uuid: 如果未设置 uuid，将使用你获取的最新 uuid
                - enableCmdQR: 在命令行中显示二维码
                - picDir: 存储二维码的地方
                - qrCallback: 应接受 uuid、状态、二维码的方法
            它定义在 components/login.py 中
        '''
        raise NotImplementedError()
    def check_login(self, uuid=None):
        ''' 检查登录状态
            选项：
                - uuid: 如果未设置 uuid，将使用你获取的最新 uuid
            返回值：
                - 将返回一个字符串
                - 返回值的含义
                    - 200: 登录成功
                    - 201: 等待按确认
                    - 408: uuid 超时
                    - 0  : 未知错误
            处理：
                - syncUrl 和 fileUrl 被设置
                - BaseRequest 被设置
            阻塞直到达到上述任何状态
            它定义在 components/login.py 中
        '''
        raise NotImplementedError()
    def web_init(self):
        ''' 获取初始化所需的信息
            处理：
                - 设置自己的账户信息
                - 设置 inviteStartCount
                - 设置 syncKey
                - 获取部分联系人
            它定义在 components/login.py 中
        '''
        raise NotImplementedError()
    def show_mobile_login(self):
        ''' 显示网页微信登录标志
            标志位于手机微信的顶部
            即使不调用此函数，标志也会在一段时间后添加
            它定义在 components/login.py 中
        '''
        raise NotImplementedError()
    def start_receiving(self, exitCallback=None, getReceivingFnOnly=False):
        ''' 打开一个线程进行心跳循环和接收消息
            选项：
                - exitCallback: 登出后的回调
                    - 包含调用 logout
                - getReceivingFnOnly: 如果为 True，将不会创建和启动线程。相反，将返回接收函数。
            处理：
                - 消息：消息被格式化并传递给注册的函数
                - 联系人：当接收到相关信息时，聊天室会更新
            它定义在 components/login.py 中
        '''
        raise NotImplementedError()
    def get_msg(self):
        ''' 获取消息
            获取时
                - 方法会阻塞一段时间，直到
                    - 新消息被接收
                    - 或者随时他们喜欢
                - synckey 会与返回的 synccheckkey 更新
            它定义在 components/login.py 中
        '''
        raise NotImplementedError()
    def logout(self):
        ''' 登出
            如果核心现在是活跃的
                登出将告诉微信后台登出
            并且核心准备好进行另一次登录
            它定义在 components/login.py 中
        '''
        raise NotImplementedError()
    def update_chatroom(self, userName, detailedMember=False):
        ''' 更新聊天室
            对于聊天室联系人
                - 聊天室联系人需要更新以获取详细信息
                - 详细信息意味着成员、encryid 等
                - 心跳循环的自动更新是更详细的更新
                    - 成员 uin 也将被填充
                - 一旦调用，更新的信息将被存储
            选项
                - userName: 聊天室的 'UserName' 键或其列表
                - detailedMember: 是否获取联系人的成员
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def update_friend(self, userName):
        ''' 更新好友
            对于好友联系人
                - 一旦调用，更新的信息将被存储
            选项
                - userName: 好友的 'UserName' 键或其列表
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def get_contact(self, update=False):
        ''' 获取部分联系人
            对于部分
                - 所有的大型平台和好友都被获取
                - 如果更新，仅获取星标聊天室
            选项
                - update: 如果未设置，将返回本地值
            结果
                - 将返回 chatroomList
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def get_friends(self, update=False):
        ''' 获取好友列表
            选项
                - update: 如果未设置，将返回本地值
            结果
                - 将返回好友信息字典的列表
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def get_chatrooms(self, update=False, contactOnly=False):
        ''' 获取聊天室列表
            选项
                - update: 如果未设置，将返回本地值
                - contactOnly: 如果设置，仅返回星标聊天室
            结果
                - 将返回聊天室信息字典的列表
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def get_mps(self, update=False):
        ''' 获取大型平台列表
            选项
                - update: 如果未设置，将返回本地值
            结果
                - 将返回平台信息字典的列表
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def set_alias(self, userName, alias):
        ''' 为好友设置别名
            选项
                - userName: 信息字典的 'UserName' 键
                - alias: 新别名
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def set_pinned(self, userName, isPinned=True):
        ''' 为好友或聊天室设置固定
            选项
                - userName: 信息字典的 'UserName' 键
                - isPinned: 是否固定
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def accept_friend(self, userName, v4, autoUpdate=True):
        ''' 接受好友请求
            选项
                - userName: 好友信息字典的 'UserName'
                - status:
                    - 添加状态应为 2
                    - 接受状态应为 3
                - ticket: 问候消息
                - userInfo: 好友的其他信息以添加到本地存储
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def get_head_img(self, userName=None, chatroomUserName=None, picDir=None):
        ''' 文档位置
            选项
                - 如果你想获取聊天室头像：只需设置 chatroomUserName
                - 如果你想获取好友头像：只需设置 userName
                - 如果你想获取聊天室成员头像：同时设置两者
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def create_chatroom(self, memberList, topic=''):
        ''' 创建聊天室
            创建时
                - 其调用频率受到严格限制
            选项
                - memberList: 成员信息字典的列表
                - topic: 新聊天室的主题
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def set_chatroom_name(self, chatroomUserName, name):
        ''' 设置聊天室名称
            设置时
                - 这将更新聊天室
                - 这意味着在心跳循环中将返回详细信息
            选项
                - chatroomUserName: 聊天室信息字典的 'UserName' 键
                - name: 新聊天室名称
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def delete_member_from_chatroom(self, chatroomUserName, memberList):
        ''' 从聊天室中删除成员
            删除时
                - 你不能删除自己
                - 如果是这样，将不会删除任何人
                - 严格限制的频率
            选项
                - chatroomUserName: 聊天室信息字典的 'UserName' 键
                - memberList: 成员信息字典的列表
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def add_member_into_chatroom(self, chatroomUserName, memberList,
            useInvitation=False):
        ''' 向聊天室添加成员
            添加时
                - 你不能添加自己或已经在聊天室中的成员
                - 如果是这样，将不会添加任何人
                - 如果添加后成员超过 40，必须使用邀请
                - 严格限制的频率
            选项
                - chatroomUserName: 聊天室信息字典的 'UserName' 键
                - memberList: 成员信息字典的列表
                - useInvitation: 如果不需要邀请，请设置为使用
            它定义在 components/contact.py 中
        '''
        raise NotImplementedError()
    def send_raw_msg(self, msgType, content, toUserName):
        ''' 许多消息以常见方式发送
            示例
                .. code:: python

                    @itchat.msg_register(itchat.content.CARD)
                    def reply(msg):
                        itchat.send_raw_msg(msg['MsgType'], msg['Content'], msg['FromUserName'])

            这里有一些小技巧，你可以自己发现
            但请记住，它们是技巧
            它定义在 components/messages.py 中
        '''
        raise NotImplementedError()
    def send_msg(self, msg='测试消息', toUserName=None):
        ''' 发送纯文本消息
            选项
                - msg: 如果消息中有非 ASCII 字符，应该是 Unicode
                - toUserName: 好友字典的 'UserName' 键
            它定义在 components/messages.py 中
        '''
        raise NotImplementedError()
    def upload_file(self, fileDir, isPicture=False, isVideo=False,
            toUserName='filehelper', file_=None, preparedFile=None):
        ''' 上传文件到服务器并获取 mediaId
            选项
                - fileDir: 准备上传的文件目录
                - isPicture: 文件是否为图片
                - isVideo: 文件是否为视频
            返回值
                将返回一个 ReturnValue
                如果成功，mediaId 在 r['MediaId'] 中
            它定义在 components/messages.py 中
        '''
        raise NotImplementedError()
    def send_file(self, fileDir, toUserName=None, mediaId=None, file_=None):
        ''' 发送附件
            选项
                - fileDir: 准备上传的文件目录
                - mediaId: 文件的 mediaId。
                    - 如果设置，文件将不会被重复上传
                - toUserName: 好友字典的 'UserName' 键
            它定义在 components/messages.py 中
        '''
        raise NotImplementedError()
    def send_image(self, fileDir=None, toUserName=None, mediaId=None, file_=None):
        ''' 发送图片
            选项
                - fileDir: 准备上传的文件目录
                    - 如果是 gif，请命名为 'xx.gif'
                - mediaId: 文件的 mediaId。
                    - 如果设置，文件将不会被重复上传
                - toUserName: 好友字典的 'UserName' 键
            它定义在 components/messages.py 中
        '''
        raise NotImplementedError()
    def send_video(self, fileDir=None, toUserName=None, mediaId=None, file_=None):
        ''' 发送视频
            选���
                - fileDir: 准备上传的文件目录
                    - 如果设置了 mediaId，则不需要设置 fileDir
                - mediaId: 文件的 mediaId。
                    - 如果设置，文件将不会被重复上传
                - toUserName: 好友字典的 'UserName' 键
            它定义在 components/messages.py 中
        '''
        raise NotImplementedError()
    def send(self, msg, toUserName=None, mediaId=None):
        ''' 所有发送函数的封装函数
            选项
                - msg: 以不同字符串开头的消息表示不同类型
                    - 类型字符串列表：['@fil@', '@img@', '@msg@', '@vid@']
                    - 它们分别用于文件、图片、纯文本、视频
                    - 如果没有匹配的类型，将像纯文本一样发送
                - toUserName: 好友字典的 'UserName' 键
                - mediaId: 如果设置，上传将不会重复
            它定义在 components/messages.py 中
        '''
        raise NotImplementedError()
    def revoke(self, msgId, toUserName, localId=None):
        ''' 撤回消息及其 msgId
            选项
                - msgId: 服务器上的消息 Id
                - toUserName: 好友字典的 'UserName' 键
                - localId: 本地消息 Id（可选）
            它定义在 components/messages.py 中
        '''
        raise NotImplementedError()
    def dump_login_status(self, fileDir=None):
        ''' 将登录状态转储到特定文件
            选项
                - fileDir: 转储登录状态的目录
            它定义在 components/hotreload.py 中
        '''
        raise NotImplementedError()
    def load_login_status(self, fileDir,
            loginCallback=None, exitCallback=None):
        ''' 从特定文件加载登录状态
            选项
                - fileDir: 加载登录状态的文件
                - loginCallback: 成功登录后的回调
                    - 如果未设置，屏幕将被清除，二维码将被删除
                - exitCallback: 登出后的回调
                    - 包含调用 logout
            它定义在 components/hotreload.py 中
        '''
        raise NotImplementedError()
    def auto_login(self, hotReload=False, statusStorageDir='itchat.pkl',
            enableCmdQR=False, picDir=None, qrCallback=None,
            loginCallback=None, exitCallback=None):
        ''' 像网页微信一样登录
            登录时
                - 将下载并打开一个二维码
                - 然后记录扫描状态，暂停以供你确认
                - 最后登录并显示你的昵称
            选项
                - hotReload: 启用热重载
                - statusStorageDir: 存储登录状态的目录
                - enableCmdQR: 在命令行中显示二维码
                    - 整数可以用于适应奇怪的字符长度
                - picDir: 存储二维码的地方
                - loginCallback: 成功登录后的回调
                    - 如果未设置，屏幕将被清除，二维码将被删除
                - exitCallback: 登出后的回调
                    - 包含调用 logout
                - qrCallback: 应接受 uuid、状态、二维码的方法
            用法
                ..code::python

                    import itchat
                    itchat.auto_login()

            它定义在 components/register.py 中
            当然，登录中的每一个动作都可以在外部调用
                - 你可以扫描源代码以查看如何
                - 并根据自己的需求进行修改
        '''
        raise NotImplementedError()
    def configured_reply(self):
        ''' 确定消息的类型并在其方法定义时进行回复
            然而，我使用了一种奇怪的方式来确定消息是否来自大型平台
            我还没有找到更好的解决方案
            我担心的主要问题是新朋友在手机上添加时的不匹配
            如果你有任何好的想法，请务必报告一个问题。我将非常感激。
        '''
        raise NotImplementedError()
    def msg_register(self, msgType,
            isFriendChat=False, isGroupChat=False, isMpChat=False):
        ''' 装饰器构造函数
            根据给定的信息返回特定的装饰器
        '''
        raise NotImplementedError()
    def run(self, debug=True, blockThread=True):
        ''' 启动自动响应
            选项
                - debug: 如果设置，将在屏幕上显示调试信息
            它定义在 components/register.py 中
        '''
        raise NotImplementedError()
    def search_friends(self, name=None, userName=None, remarkName=None, nickName=None,
            wechatAccount=None):
        return self.storageClass.search_friends(name, userName, remarkName,
            nickName, wechatAccount)
    def search_chatrooms(self, name=None, userName=None):
        return self.storageClass.search_chatrooms(name, userName)
    def search_mps(self, name=None, userName=None):
        return self.storageClass.search_mps(name, userName)
