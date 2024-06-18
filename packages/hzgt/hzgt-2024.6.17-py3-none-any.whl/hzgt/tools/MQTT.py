import os
import threading

from ..strop import restrop
from ..CONST import INSTALLCMD
from ..sc import SCError

try:
    import paho.mqtt.client as mqtt
except Exception as err:
    print(err)
    os.system(INSTALLCMD("paho-mqtt==1.6.1"))
    import paho.mqtt.client as mqtt

class Mqttop:
    def __init__(self, mqtt_host: str, mqtt_port: int, mqtt_clientid: str = '', mqtt_subtopic: str = '',
                 user: str = '', pwd: str = '', bool_show: bool = True, bool_clean_session: bool = False):
        """
        调用self.publish()函数发布信息

        :param mqtt_host: MQTT服务器IP地址
        :param mqtt_port: MQTT端口
        :param mqtt_clientid: 可选, "客户端"用户名 为空将随机
        :param mqtt_subtopic: 选填, 需要订阅的主题 通过self.got_datas获得接收到的信息 为空时仅连接[此时可进行发布信息]; 更换订阅主题需要使用self.retopic()函数[自动重连]

        :param user: 选填, 账号
        :param pwd: 选填, 密码
        """
        self.got_datas: str = None  # 接收到的数据
        self.bool_show = bool_show  # 是否终端打印连接相关信息
        self.bool_con_success = False  # 是否连接成功
        self.bool_clean_session = bool_clean_session  # 在断开连接时是否删除有关此客户端的所有信息, 若mqtt_clientid参数为空, 将强制为True

        self.mqtt_host = mqtt_host
        self.mqtt_port = int(mqtt_port)
        self.mqtt_clientid = mqtt_clientid
        self.mqtt_subtopic = mqtt_subtopic
        self.user = user
        self.pwd = pwd

        if len(self.mqtt_clientid) == 0 or self.mqtt_clientid is None:
            self.client = mqtt.Client(client_id="", clean_session=True)  # 创建对象, 强制clean_session=True
        else:
            self.client = mqtt.Client(client_id=self.mqtt_clientid, clean_session=self.bool_clean_session)  # 创建对象
        # self.start()

    def __del__(self):
        """
        删除对象时调用__del__()断开连接
        """
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return exc_type, exc_val, exc_tb

    def set_will(self, will_topic: str, will_msg: str):
        """
        设置遗嘱, 需要在连接前设置
        :param will_topic: 遗嘱主题
        :param will_msg: 遗嘱信息
        """
        self.client.will_set(will_topic, will_msg, 0, False)
        print(f"遗嘱信息: will_topic[`{restrop(will_topic, f=6)}`] will_msg[`{restrop(will_msg, f=4)}`] 已设置")

    def start(self):
        """
        启动MQTT连接, 建议使用time.sleep(5)等待连接完成
        :return:
        """
        threading.Thread(target=self.__run, daemon=True).start()  # 开启线程防止阻塞主程序, 使用.close()函数自动关闭该线程

    def close(self):
        """
        断开MQTT连接
        """

        # 断开MQTT连接
        self.client.disconnect()
        # 停止循环
        self.client.loop_stop()

        if self.bool_show:
            print(restrop("MQTT连接已关闭"))

        self.bool_con_success = False

    # 断开连接回调
    def __on_disconnect(self, client, userdata, rc):
        """

        """
        if self.bool_show and self.bool_con_success:
            print(f"MQTT连接已断开")
        self.bool_con_success = False

    # 连接后事件
    def __on_connect(self, client, userdata, flags, respons_code):
        """
        respons_code的含义\n
        0:连接成功\n
        1:连接被拒绝-协议版本不正确\n
        2:连接被拒绝-客户端标识符无效\n
        3:连接被拒绝-服务器不可用\n
        4:连接被拒绝-用户名或密码错误\n
        5:连接被拒绝-未授权\n
        6-255:当前未使用\n

        :param client:
        :param userdata:
        :param flags:
        :param respons_code:
        :return:
        """
        if respons_code == 0:
            # 连接成功
            if self.bool_show:
                print(restrop('MQTT服务器 连接成功!', f=2))
            self.bool_con_success = True
        else:
            # 连接失败并显示错误代码
            if self.bool_show:
                print(restrop(f'连接出错 rc={respons_code}'))
            self.bool_con_success = False
        # 订阅信息
        if self.mqtt_subtopic:
            self.client.subscribe(self.mqtt_subtopic)
            if self.bool_show:
                print(f"当前订阅的主题: `{restrop(self.mqtt_subtopic, f=4)}`")

    # 接收到数据后事件
    def __on_message(self, client, userdata, msg):
        self.got_datas = msg.payload

    # 启动连接
    def __run(self):
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.client.on_disconnect = self.__on_disconnect
        # 设置账号密码
        if self.user:
            client.username_pw_set(username, password=password)
        # 连接到服务器
        self.client.connect(self.mqtt_host, port=self.mqtt_port, keepalive=60)
        # 守护连接状态
        self.client.loop_forever()

    # 发布消息
    def publish(self, topic: str, msg: str, bool_show_tip: bool = True):
        """

        :param topic: 发布消息的主题
        :param msg: 需要发布的消息
        :param bool_show_tip: 是否打印是否发送成功的信息
        :return:
        """
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0 and bool_show_tip:
            print(f"{restrop('发送成功', f=2)} TOPIC[`{restrop(topic, f=6)}`]  MSG[`{restrop(msg, f=4)}`]")
        elif bool_show_tip:
            print(f"{restrop('发送失败')} TOPIC[`{restrop(topic, f=6)}`]  MSG[`{restrop(msg, f=4)}`]")

    def retopic(self, new_topic: str):
        """
        更换订阅的主题, 并自动尝试重连
        :param new_topic: 新的订阅主题
        :return:
        """
        if self.mqtt_subtopic != new_topic:
            self.mqtt_subtopic = new_topic

            if self.bool_show:
                print(restrop("已更换订阅的主题, MQTT服务器正在尝试重连. . .", f=3))

            self.reconnect()

    def reconnect(self):
        """
        尝试重连
        :return: None
        """
        self.close()
        self.start()
