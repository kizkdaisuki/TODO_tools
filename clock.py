class Clock:

    def __init__(self, time):
        self.time = time

    def print_time(self):
        print(self.time)

    def start_clock(self):
        # TODO
        # 通过调用shell脚本并新开一个进程 到指定时间播放闹钟 并关闭进程
        pass

if __name__ == '__main__':
    clock = Clock('10:30')
    clock.print_time()
    clock.start_clock()