import calendar
import os
from datetime import datetime, timedelta
import logging
import re
import sys
import argparse
import os
from typing import Any, Dict, Optional  # 类型注解
from jinja2 import Environment, FileSystemLoader
import json
from requests import head


# PS:处理日期真的是个很难的时期ww特别是进位等等
# 原则：不相信任何来自文件的数据，全部关键索引都依赖硬计算
# 此文件系统可以移植到读研的日记/工作日记/考研日记，等等

# pip install --upgrade setuptools wheel目录构造如下：
"""
工作日报文档 / 一般在docs目录下
(ps：因为可能只实习3-4个月，所以直接按周归档。后续应该可以按年->月->周归档，同时做了curr移入移出)
|-- archivingFile归档文件
|-- Common常用功能
    |-- daily.py
    |-- 模板文件（日报模板/周报模板等）
    |-- 日报模板.md
    |-- 周报模板.md
|-- dailyReport日报 ---后续目录可以调整(自动归档)
    |-- archivingFile(归档文件，暂时考虑按照日期排列)
    |-- 04-24-week1
        |-- common(工作流文档 比如一些项目的文档，在完成任务后应该放入归档；未完成的自动移至下周的common目录，日报里应该只存日报而不应该有其他东西/临时文档为了方便编辑也可以放入)
        |-- 04-24.md
        |-- 04-25.md
        |-- week1周报.md
    |-- 05-06-week2
    |-- 05-13-week3
|--docsOutput文档输出
"""


"""
合法性检查类，用于提高安全
"""
class Validator:
    def __init__(self):
        pass

def main():
    # 用户输入
    # user_input = input("请输入一些数据: ")

    # todo：打包成轮子 直接命令行调用daily run xxx 而不是 python dailt.py run xxx...
    # 创建解析器和添加参数
    """
    接收参数/实现功能：
    (缺省)只建立文件夹+不打log python daily.py
    """
    parser = argparse.ArgumentParser(description="Process command line arguments")
    parser.add_argument(
        "action",
        choices=["start", "dev", "build"],
        help="Action to perform",
        nargs="?",
        const="start",
    )
    # 【指定日期】传参格式：mm-dd
    parser.add_argument(
        "-d",
        "--date",
        type=str,
        help="选择生成的日期 Choose date to generate",
        default=datetime.now().strftime("%m-%d"),
    )
    # 【指定路径】默认为调用
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="指定路径",
        default=os.getcwd(),  # 相当于. 但是返回绝对路径
    )
    # 给文件名后面加一个说明 比如04-24-入职第一天
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        help="Extra Content to write to the file",
        default="None",
    )
    args = parser.parse_args()
    # 不可靠输入：校验参数是否合法【同时把date转为datetime格式】
    args.date = DateHandler.validate_date(args.date)
    if not Utils.validate_path(args.path):
        print("路径参数不合法！请重新输入")
        return
    if args.date is None:
        print("日期参数不合法！请重新输入")
        return

    # test()
    # 工作流处理对象
    # handler = WorkFlowHandler(args)
    handler = DailyReportHandler(args)

    # 输出结果
    print("处理完成")


# 如果脚本直接运行，执行main函数
if __name__ == "__main__":
    main()
