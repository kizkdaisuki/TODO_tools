import time
from dateutil import parser
from datetime import datetime, timedelta

class GetTime:
    def __init__(self):
        pass

    @staticmethod
    def static_method_get_datetime(cur_time: datetime = None) -> str:
        t = time.localtime()
        if cur_time:
            t = cur_time
        return str(time.strftime("%Y-%m-%d %H:%M:%S", t))

    @staticmethod
    def static_method_get_date(cur_time: datetime = None) -> str:
        t = time.localtime()
        if cur_time:
            t = cur_time
        return str(time.strftime("%Y-%m-%d", t))

    @staticmethod
    def static_method_get_time(cur_time: datetime = None) -> str:
        t = time.localtime()
        if cur_time:
            t = cur_time
        return str(time.strftime("%H:%M:%S", t))

    @staticmethod
    def static_method_get_cur_week() -> int:
        return int(time.localtime().tm_wday)

    @staticmethod
    # 获得本月的天数
    def static_method_get_this_month() -> int:
        return int(str(time.strftime("%Y-%m-%d", time.localtime())).split('-')[-1])

    @staticmethod
    def static_method_get_diff_from_2_day(day1: str, day2: str) -> int:
        if day1 == '':
            day1 = '1917-02-03'
        if day2 == '':
            day2 = '1917-02-03'
        return abs(int((parser.parse(day1) - parser.parse(day2)).days))
    @staticmethod
    def static_method_add_time(time1: str, add_time_sec: int) -> str:
        t1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
        res = t1 + timedelta(seconds=add_time_sec)
        t1 = res.strftime("%Y-%m-%d %H:%M:%S")
        return t1


    @staticmethod
    def static_method_get_diff_from_2_time(time1: str, time2: str) -> [int, int]:
        t1, t2 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S"), datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
        lv_diff = t2 - t1
        lv_day_dif = lv_diff.days
        lv_sec_dif = lv_diff.seconds
        return lv_day_dif, lv_sec_dif


    @staticmethod
    def static_method_from_time_get_second(t) -> int:
        if t == 0 or t == '0' or t == '':
            return 0
        res = [0] * 3
        if t.find(':') != -1:
            t = t.split(':')
            res = [int(i) for i in t]
        elif t.find('-') != -1:
            t = t.split('-')
            res = [int(i) for i in t]
        else:
            lv_flg = True
            if t.find("min") != -1:
                lv_flg = False
            for i, k in enumerate(["h", "m" if lv_flg else "min", "s"]):
                if t.find(k) != -1:
                    l, r = t.split(k)
                    l = int(l)
                    t = r
                    res[i] = l
        return 3600 * res[0] + 60 * res[1] + res[2]
    @staticmethod
    def static_method_get_time_from_second(t: int) -> str:

        h = t // 3600
        t %= 3600
        m = t // 60
        t %= 60
        s = t
        return f'{h}h{m}m{s}s'
