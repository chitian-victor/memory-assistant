import math
from utils.deal_time import *

def cal_item_weight(item):
    first_interval=get_interval(item.create_time)
    last_interval=get_interval(item.last_time)
    return cal_ebbinghaus_with_newness(first_interval,last_interval,item.forget_times)

def cal_ebbinghaus_with_newness(days_first,days_last, forget_count):
    """
    基于艾宾浩斯公式 (0~100)
    :param days_last: 距离上次背诵的间隔天数
    :param forget_count: 不认识的次数
    :param days_first: 距离首次添加的总天数
    """
    # 1. 计算传统的艾宾浩斯遗忘概率 (0~100)
    base_strength = 7.0
    strength = base_strength / (1 + 0.8 * forget_count)
    # 避免days_last为0时出现100%保留率无法产生权重，最低给0.1
    retention = math.exp(-max(days_last, 0.1) / strength)
    ebb_score = (1 - retention) * 100

    # 2. 计算新词强力加权系数 (指数衰减，这里设半衰期约1.4天)
    # 刚添加时(1天内)为0分，1-2天为100分，2-3天为60分，4-5天为 36分，完全衰减后依靠遗忘概率
    newness_score = 100 * math.exp(-0.5 * days_first)
    if days_first<1:
        newness_score=0

    # 3. 平滑融合算法：底分为新词分，剩下的空间由遗忘分数填补
    final_score = newness_score + (1 - newness_score / 100.0) * ebb_score
    return round(final_score, 2)

if __name__ == '__main__':
    # 测试用例: ( 首次添加天数, 上次背诵天数, 忘记次数)
    test_cases = [
        (0, 0, 0),  # 今天刚加的新词，从未背过
        (1, 0, 1),  # 昨天加的词，昨天背过一次
        (1, 1, 1),  # 昨天加的词，昨天背了但没记住 (忘1次)
        (10, 0, 1),  # 10天前的老词，昨天刚复习过 (不需要背)
        (10, 0, 7),  # 10天前的老词，7天前复习过 (该复习了)
        (10, 3, 7),  # 10天前的老词，7天前复习过，且累计忘过3次 (重灾区！)
    ]
    print(f"{'上次复习':<8} | {'忘次数':<8} | {'首次添加':<8} | {'结果':<15}")
    print("-" * 75)
    for dl, f, df in test_cases:
        w = cal_ebbinghaus_with_newness(dl, f, df)
        print(f"{dl:<12} | {f:<10} | {df:<12} | {w:<20}")
