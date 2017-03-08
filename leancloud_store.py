#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import leancloud
from leancloud import Object
#from leancloud import Query
import os
import random
from utils import timestamp2time

# 设置环境变量
# set -x  LEANCLOUD_APP_ID xxx | except
# todo 不必默认执行吧
APP_ID = os.environ.get("LEANCLOUD_APP_ID")
APP_KEY = os.environ.get("LEANCLOUD_APP_KEY")
leancloud.init(APP_ID, APP_KEY)


class MessageModel(Object):
    pass

'''
messageModel = leancloud.Object.extend('messageModel')
message_model = messageModel()

message_model.set('init_message', 'go!')
message_model.save()
# self.set('content', value)
'''


def push_message(message):
    # todo:使用魔法参数
    # message is dict
    message_model = MessageModel()
    for key in message:
        message_model.set(key, message.get(key))
    message_model.save()

def message2cloud(msg):
    '''
    for ai100
    所有群消息都存下来，任何的群都为其建立映射 群名映射
    itchat.search_chatrooms(userName='@@abcdefg1234567') #建立缓存
    # 分解： 把头像部分抽象为函数，把群名获取抽象为函数 把缓存考虑在内
    https://github.com/youfou/wxpy
    '''
    message2push={}
    message2push["content"] = msg["Text"]
    message2push["group_user_name"] = msg["ActualNickName"]
    message2push["CreateTime"] = timestamp2time(int(msg["CreateTime"]))
    push_message(message2push)


def save_file(filename, data):
    # data_hash = hashlib.md5(data).hexdigest() # 一致 26771cad667b860261090a8d52f3299c wwj 缓存在user_img_cache里做
    # https://leancloud.cn/docs/leanstorage_guide-python.html#从数据流构建文件
    cloud_file = leancloud.File(filename, data)
    cloud_file.save()
    return cloud_file.url


def main():
    for i in range(1, 501):
        message = {}
        message["group_name"] = random.choice(["小组1", "小组2", "小组3", "小组4"])
        message["content"] = "这是第{}条消息".format(i)
        message["group_user_name"] = "群友-{}".format(random.randint(1, 20))
        push_message(message)

if __name__ == '__main__':
    main()
