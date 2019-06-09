'''
@author: qujb
@contact: 15210825203@163.com
@file: User_interaction.py
@time: 2019/6/7 上午8:26
@desc:
'''
from src.common.common import register_user,validate_user,turn_2_user,get_top5
from src.Mongo_deploy import MongoConn
from random import random
class UserInterface():
    def __init__(self):
        # self.t =  MongoConn("Hong Kong")
        self.t = None
        while True:
            to_find = input('''
            请输入你想要查询的内容：
            1.用户登陆
            2.热榜
            4.注册
            5.q退出
            ''')
            if to_find == '1' :
                while True:
                    user_name = input('请输入用户名:(q退出)')
                    if user_name == 'q':
                        break
                    if user_name is None or len(user_name) < 5 :
                        print('请输入有效的用户id')
                    else:
                        self.t,flag = validate_user(user_name)
                        if flag:
                            turn_2_user(self.t,user_name)
                            break
                        else:
                            print('用户名错误')

            elif to_find == '2':

                region = "Beijing" if random()>0.4 else "Hong Kong"
                t = MongoConn(region)
                get_top5(t)
            # elif to_find =='3':
            #     article_id = input("请输入文章id：")
            #         show_article(self.t,article_id)
            elif to_find == '4':
                user_id = input('请输入用户id进行注册:(q退出)')
                if user_id == 'q':
                    continue
                user = register_user(self.t, user_id)
                if user is None:
                    print('该用户已经存在，请直接登录')
                else:
                    print('注册成功')
            elif to_find == 'q':
                break
            else:
                print('请输入正确的查询码')


if __name__ == '__main__':
    print('here we  are')
    UI = UserInterface()