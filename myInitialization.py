__author__ = 'Luzaofa'
__date__ = '2019/1/19 10:44'

import time
import datetime
import multiprocessing as mp
from apscheduler.schedulers.blocking import BlockingScheduler


class Demo(object):

    def __init__(self):
        pass

    def data_mp(self, func, mass):
        '''进程池'''
        pool = mp.Pool(processes=4)
        for i in mass:
            pool.apply_async(func, args=(i,))
        pool.close()
        pool.join()

    def scheduler(self, func, args):
        '''时间管理器'''
        sched = BlockingScheduler()
        print('初次执行时间: ', (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"))
        sched.add_job(func, 'interval', seconds=60, args=(args,), id='my_job1')  # 每隔一分钟执行一次
        # sched.add_job(func, 'cron', day_of_week='mon-fri', hour=17, minute=00, args=mass, id='my_job2')  # 工作日下午5点执行
        sched.start()

    def log(self, fileName, mass):
        '''日志'''
        with open(fileName, 'a+') as f:
            f.writelines(str(mass) + '\n')
            f.flush()

    def logic(self, mass):
        '''
        业务逻辑
        :param mass:
        :return:
        '''
        self.log('log.txt', mass)

    def main(self, mass):
        '''
        主入口
        :return:
        '''
        start = time.time()
        self.data_mp(self.logic, mass)
        end = time.time()
        print('业务处理总耗时：%s 秒！' % (end - start))
        print('下次执行时间: ', (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == '__main__':
    print('Start！')
    demo = Demo()
    mass = [i for i in range(100)]

    # demo.main(mass)  # 多进程

    demo.scheduler(demo.main, args=mass)  # 定时 + 多进程

    print('END')
