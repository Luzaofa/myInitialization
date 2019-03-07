__author__ = 'Luzaofa'
__date__ = '2019/3/7 21:08'

import time
import datetime
import logging
import configparser
import multiprocessing as mp
from apscheduler.schedulers.blocking import BlockingScheduler


class Config(object):
    '''解析配置文件'''

    def get_config(self, lable, value):
        cf = configparser.ConfigParser()
        cf.read("CONFIG.conf")
        config_value = cf.get(lable, value)
        return config_value


class Demo(Config):

    def __init__(self):
        '''读取配置文件夹信息初始化 [lable] value = value'''
        super(Config, self).__init__()
        # self.arg1 = self.get_config('lable', 'value')

    def data_mp(self, func, pros):
        '''进程池'''
        pool = mp.Pool(processes=4)
        for pro in pros:
            pool.apply_async(func, args=(pro,))
        pool.close()
        pool.join()

    def scheduler(self, func):
        '''时间管理器'''
        sched = BlockingScheduler()
        print('初次执行时间: ', (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"))
        sched.add_job(func, 'interval', seconds=60, id='my_job1')  # 每隔一分钟执行一次
        # sched.add_job(func, 'cron', day_of_week='mon-fri', hour=17, minute=00, args=mass, id='my_job2')  # 工作日下午5点执行
        sched.start()

    def log(self, fileName, mass):
        '''日志'''
        logging.basicConfig(filename=fileName, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.info(mass)

    def logic(self, args):
        '''
        业务逻辑（单个任务逻辑模块）
        '''
        print(args)

    def main(self):
        '''
        主入口
        :return:
        '''
        start = time.time()
        pros = [1]  # 任务池
        # self.logic(pros)  # 普通处理
        self.data_mp(self.logic, pros)  # 多进程
        end = time.time()
        print('业务处理总耗时：%s 秒！' % (end - start))
        print('下次执行时间: ', (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == '__main__':
    print('Start！')
    demo = Demo()

    demo.main()  # 普通
    # demo.scheduler(demo.main)  # 定时

    print('END')
