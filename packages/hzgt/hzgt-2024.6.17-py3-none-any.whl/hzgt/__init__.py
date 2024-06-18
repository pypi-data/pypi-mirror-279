import os
import sys

# 版本
from ._version import __version__
version = __version__

# 字符串操作
from .strop import getmidse, pic, restrop, restrop_list

# 字节单位转换
from .fileop import bit_unit_conversion

# 获取文件大小
from .fileop import get_file_size, get_urlfile_size

# 装饰器 gettime获取函数执行时间
from .Decorator_ import gettime, timelog

# 文件 / github仓库 / 视频 下载
from .download.download import downloadmain

# ======================================================= tools =======================================================
# MQTT 和 MYSQL
from .tools.MQTT import Mqttop
from .tools.MYSQL import Mysqldbop
# 函数注册器 / 类注册器
from .tools.REGISTER import Func_Register, Class_Register
# FTP服务端 / FTP客户端
from .tools.FTP import Ftpserver, Ftpclient
# 读取ini文件 / 保存ini文件
from .tools.Iniop import readini, saveini
# ======================================================= tools =======================================================


