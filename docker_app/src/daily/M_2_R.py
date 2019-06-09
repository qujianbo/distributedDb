'''
@author: qujb
@contact: 15210825203@163.com
@file: M_2_R.py
@time: 2019/6/9 上午7:55
@desc: 这个文件定义每天redis从mongo那里获取更新数据
'''
import os
import datetime
from src.common.funcOfRedis import r1,r2
from src.common.funOfMongo import t1,t2,generate_be_read,generate_pop

class SynchronizeService:
    def __init__(self):
        pass
    # 计算mongo中的be_read表和pop表
    def mongo_calculate(self):
        generate_be_read(t1,t2)
        generate_be_read(t2,t1)
        generate_pop(t1)
        generate_pop(t2)
    # Key: “Popular_Rank” +temporalGranularity
    def sync_pop(self,M,R,temporalGranularity):
        pop_collection = M.get_single_doc("pop_rank",temporalGranularity)["articleList"]
        insert_key = "Popular_Rank" + temporalGranularity
        for i in range(5,0,-1):
            R.lpush(insert_key,pop_collection[i])
    # 这里写具体的同步逻辑
    def synchronize(self):
        # 先搞定热搜
        

    def timerFun(self,schedTimer):
        flag = 0
        while True:
            now = datetime.datetime.now()
            if now == schedTimer:
                self.mongo_calculate()
                self.synchronize()

                flag = 1

            else:
                if flag == 1:
                    schedTimer = schedTimer + datetime.timedelta(days=1)
                    flag = 0

if __name__ == '__main__':
    ss = SynchronizeService()
    schedTimer = datetime.datetime(2019,6,9,8,0)
    print('run the timer task at {0}'.format(schedTimer))
    ss.timerFun(schedTimer)