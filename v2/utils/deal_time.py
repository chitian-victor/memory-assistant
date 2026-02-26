import time
from datetime import datetime

FORMAT_PATTERN = "%Y-%m-%d %H:%M:%S"
DAY_SECONDS = 3600 * 24

def format_current_time():
    """获取当前时间的格式化字符串"""
    now = datetime.now()
    return now.strftime(FORMAT_PATTERN)


def get_interval(last_time_str):
    """
    计算给定时间字符串距离现在的天数间隔
    :param last_time_str: 上次记录的时间字符串
    """
    dt = datetime.strptime(last_time_str, FORMAT_PATTERN)
    last_time = dt.timestamp()
    now = time.time()

    return round((now - last_time) / DAY_SECONDS, 2)


if __name__ == '__main__':
    # 测试变量
    test_time_str = "2026-02-25 17:42:00"

    print(get_interval(test_time_str))
    print(format_current_time())