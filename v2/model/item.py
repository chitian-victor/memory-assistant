from utils.cal_weight import cal_item_weight
class ItemCls:
    def __init__(self,data,create_time,last_time,forget_times,weight=0):
        self.data: str=data
        self.create_time: str=create_time
        self.last_time: str=last_time
        self.forget_times: int=forget_times
        self.weight: int=weight
    def update_last_time(self,new_last_time):
        self.last_time=new_last_time
        self.weight= cal_item_weight(self)
    def update_forget_times(self,new_forget_times):
        self.forget_times = new_forget_times
        self.weight = cal_item_weight(self)

def print_items(items):
    # 1. 定义表格表头
    headers = ["词条", "创建时间", "最后复习时间", "遗忘次数", "权重"]
    # 定义列宽（根据内容调整，保证对齐）
    col_widths = [10, 20, 20, 8, 8]

    # 2. 打印表头
    header_line = "|".join([f"{header:<{col_widths[i]-len(header)+i}}" for i, header in enumerate(headers)])
    print("+" + "+".join(["-" * w for w in col_widths]) + "+")
    print(f"|{header_line}|")
    print("+" + "+".join(["-" * w for w in col_widths]) + "+")

    # 3. 打印每行数据
    for item in items:
        # 提取实例的属性值，按列整理
        row_data = [
            item.data,
            item.create_time,
            item.last_time,
            str(item.forget_times),  # 转为字符串便于对齐
            f"{item.weight:.2f}"  # 权重保留1位小数
        ]
        # 格式化每行内容（左对齐，填充空格）
        row_line = "|".join([f"{data:<{col_widths[i]}}" for i, data in enumerate(row_data)])
        print(f"|{row_line}|")

    # 4. 打印表格底部边框
    print("+" + "+".join(["-" * w for w in col_widths]) + "+")

if __name__ == '__main__':
    # 创建测试实例（模拟单词数据）
    item1 = ItemCls("apple", "2026-02-01 08:00:00", "2026-02-24 10:00:00", 2, 78.5)
    item2 = ItemCls("banana", "2026-02-05 09:00:00", "2026-02-25 12:00:00", 5, 92.3)
    item3 = ItemCls("orange", "2026-02-10 11:00:00", "2026-02-23 15:00:00", 1, 45.8)

    # 实例列表（待输出的数据源）
    item_list = [item1, item2, item3]
    print_items(item_list)
