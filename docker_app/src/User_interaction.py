'''
@author: qujb
@contact: 15210825203@163.com
@file: User_interaction.py
@time: 2019/6/7 上午8:26
@desc:
'''
from src.common.common import register_user,validate_user,turn_2_user,get_top5
from src.Mongo_deploy import MongoConn
class UserInterface():
    def __init__(self):
        self.t =  MongoConn("Hong Kong")
        while True:
            to_find = input('''
            请输入你想要查询的内容：
            1.用户登陆
            2.热榜
            3.文章
            4.注册
            5.q
            ''')
            if to_find == '1' :
                while True:
                    user_name = input('请输入用户名:')
                    if int(user_name[4:]) > 10000:
                        print('请输入有效的用户id')
                    else:
                        if validate_user(self.t,user_name):
                            turn_2_user(self.t,user_name)
                            break
                        else:
                            print('用户名错误')


            elif to_find == '2':
                # get_top5()
                pass
            elif to_find =='3':
                pass
            elif to_find == '4':
                user_id = input('请输入用户id进行注册:')
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