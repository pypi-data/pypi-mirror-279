import calendar
import os
from datetime import datetime, timedelta
import logging
from jinja2 import Environment, FileSystemLoader
from requests import head

# 导入本地包
from utils import DateHandler, Utils
from template import Template

# 日报类，主要处理日报+周报处理【逻辑核心】
class DailyReportHandler:
    def __init__(self, cmd, *args, **kwargs) -> None:
        # 参数初始化
        self.parse_args(cmd, *args, **kwargs)
        # 路径初始化，支持多种路径下调用【含cmd里，含校验，或者】
        self.__init_path()
        # 读取config文件(同时处理日期)+更新
        self.config = self.parse_config()
        self.config = Template.update_daily_config(self.arg_date,self.config)
        print(self.config)
        # 这个offsets可以复用，项目为：offset_days offset_weeks curr_monday first_monday
        self.offset = DateHandler.get_date_offsets(self.config,self.arg_date)
        # 获取daily下对于目录
        dir_name =  self.get_weekly_dir_name()
        # 检查日报周报是否存在，存在则直接结束,不存在则创建日报（周报会选择性处理）
        if not self.checkDailyReportExist(dir_name,self.arg_date):
            # 写入config文件【写入最新后，才生成日报与周报（确保不重复）】
            json_path = os.path.join(self.path["root"], "config.json")

            Utils.write_json(self.config,json_path)
            # 周报处理
            self.create_weekly_report(dir_name)
            # 日报处理
            self.create_daily_report(dir_name)


    # 参数初始化
    def parse_args(self, cmd, *args, **kwargs):
        # self.arg_action = cmd.action
        self.arg_date = cmd.date
        self.arg_path = cmd.path
        self.arg_action = cmd.action
        self.arg_message = cmd.message
        # 其他参数：暂未确定

    # 解析config参数(如果为空，则要创建default_config)
    def parse_config(self):
        config_file = os.path.join(self.path["root"], "config.json")
        config = {}
        if not os.path.exists(config_file):
            print("json文件不存在,正在创建ing")
            config = Template.create_default_config(self.arg_date)
        else:
            print("检测到json文件，正在读取")
            config = Utils.read_json(config_file)
            if config == None: # 检查config格式，todo
                pass            
        # print("读取到基本信息：\n",str(self.config["global"]))
        return config

        
    # 以传入的路径[arg.path 一般是命令调用的路径]为根路径，动态寻找父目录是否存在，没有则提示创建【算法知识】
    def __init_path(self):
        print("当前目录为" + self.arg_path)

        base_dir = self.arg_path
        base_dir_list = [
            "archivingFile归档文件",
            "Common常用",
            "dailyReport日报",
            "docsOutput文档输出",
        ]
        flag = False  # 要4个目录都存在，才判定为基目录

        # 最多遍历4级父目录(更多有一点不礼貌了)
        for i in range(0, 4):
            if not all([os.path.exists(os.path.join(base_dir, name)) for name in base_dir_list]):
                base_dir = os.path.dirname(base_dir)  # 切换父级目录
                # print(f"切换到父级目录为{base_dir}")
                continue
            else:
                flag = True
                print(f"找到基目录为{base_dir}")
                break
        if not flag:
            # 创建目录 直接以arg.path为基目录
            user_input = input(f"基目录不存在，输入y/Y创建目录在{self.arg_path}：")
            if(user_input in ["y","Y"]):
                print("正在创建目录")
                base_dir = self.arg_path    # 把base_dir回到参数的目录上
                for name in base_dir_list:
                    os.makedirs(os.path.join(self.arg_path, name)) if not os.path.exists(os.path.join(self.arg_path, name)) else None
            else :
                print("用户退出")
                exit(0)
        self.path = {
            "root": base_dir,
            "archivingFile": os.path.join(self.arg_path, "archivingFile归档文件"),
            "common": os.path.join(self.arg_path, "Common常用"),
            "dailyReport": os.path.join(self.arg_path, "dailyReport日报"),
            "docsOutput": os.path.join(self.arg_path, "docsOutput文档输出"),
        }
        pass
    

    """get_weekly_dir_name 获取周报文件夹名称
    description:周报文件夹由”当周日期-当前周数“组成，如
        # 检查传入的日期是否创建了相应的目录（weekx）
        # 如传入04-26,要检查其在04-24-week1目录下
    Returns:
        _type_: _description_
    """
    def get_weekly_dir_name(self):        
        week_file_name = self.offset["curr_monday"]+"-week"+str(self.offset["offset_weeks"])
        print("正在检查所在周目录：",week_file_name)
        # 检查是否存在
        if not os.path.exists(os.path.join(self.path["dailyReport"],week_file_name)):
            pass
            print("目录不存在，正在创建",week_file_name)
            os.makedirs(os.path.join(self.path["dailyReport"],week_file_name))
        else :
            print("目录已经存在")
        
        return week_file_name

    """checkDailyReportExist 检查日报是否存在
    description:
    Returns:
        _type_: _description_
    """
    def checkDailyReportExist(self,dir_name,arg_date):
        file_path = os.path.join(dir_name,arg_date.strftime("%m-%d")+".md")
        if os.path.exists(file_path):
            print("日报已经存在")
            return True
        else:
            print("日报不存在")
            return False

    # 从config中获取需要填充的数据;日报数据里的变量可以参考readme
    def get_daily_data(self):
        # 初始化一个数据结构，缺省值
        filled_data = {
            "day": 1,
            "week": 1,
            "type": "日",
            "ip": "http://10.10.41.235:8001/",
            "curr_date": self.arg_date.strftime("%Y-%m-%d"),
        }
        filled_data["day"] = self.config["global"]["work_day"]
        filled_data["week"] = self.config["global"]["work_week"]
        filled_data["curr_date_badage"] = self.arg_date.strftime("%m--%d")
        return filled_data

        
    # 填充周报的模板数据，模板参考readme:weekly_test_data{date,content,class,ip}
    def get_weekly_report_data(self):
        __template = Template.weekly_template_vars
        __offset = DateHandler.get_date_offsets(self.config,self.arg_date)
        __dir_name = str(__offset["curr_monday"])+'-week'+str(__offset["offset_weeks"])
        
        __report_data = []
        for index in self.config["detail"][__offset["offset_weeks"]-1]["date"]:
            __report_data.append({
                "date": index,
                "content": "",
                "class":"",
                "link":"["+index+"-邓仕昊的工作日报"+"](http://10.10.41.235:8001/dailyReport日报/"+__dir_name+"/"+index+"/)"
            })

        __template.update({
            "week": __offset["offset_weeks"],
            "day": __offset["offset_days"],
            "type": "周",
            "ip": "http://10.10.41.235:8001/",
            "curr_date": self.arg_date,
            "curr_date_badage": "week"+str(__offset["offset_weeks"]),
            # 有部分数据没更新，只是提前把接口变量写上了
            "weekly_report_data": __report_data
        })

        return __template

     
    # 生成周报(暂时只有周五周六才生成，没找到更好的办法)
    def create_weekly_report(self,dir_name):
        # 检查是否要生成周报：一周的每一天都检查一次，如果没有这个文件就生成
        file_path = os.path.join(self.path["dailyReport"],dir_name,"week"+str(self.offset["offset_weeks"])+"周报.md")
        if not os.path.exists(file_path) and self.arg_date.weekday() in [4,6]:
            print("正在生成周报",file_path)
            fill_data = self.get_weekly_report_data()
            Template.render_template(fill_data, file_path)

        # 检查是否是新的一周，要迁移common目录【未完成】
        # if self.arg_date.weekday() == 0 and self.config["global"]["work_week"] != self.get_week_offset()["offset_weeks"]:
        #     print("正在迁移common目录",self.path["dailyReport"],self.path["common"],dir_name)
        #     # 迁移common目录
        #     shutil.move(self.["common"],os.path.join(self.path["dailyReport"],dir_name))

    def create_daily_report(self,dir_name):
        # 检查是否要生成日报
        file_path = os.path.join(self.path["dailyReport"],dir_name,self.arg_date.strftime("%m-%d")+".md")
        if not os.path.exists(file_path):
            print("正在生成日报",file_path)
            fill_data = self.get_daily_data()
            Template.render_template(fill_data, file_path)
        else:
            print("日报已经存在")

def main():
    # 测试这个类
    from argparse import Namespace
    from datetime import datetime, timedelta
    import time

    # 起始日期设为2024年4月1日
    start_date = datetime(2024, 4, 24)
    # 结束日期设为2024年6月30日
    end_date = datetime(2024, 5, 10)

    # 循环遍历指定日期范围内的每一天
    for single_date in (start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)):
        # 构造Namespace对象
        args_instance = Namespace(
            action=None,
            date=single_date,
            message='None',
            path='D:\\code\\github\\dailyReportHandler\\.temp'
        )
        
        # 打印或进一步处理args_instance
        print(args_instance)
        handler = DailyReportHandler(args_instance)
        time.sleep(5)

if __name__ == "__main__":
    main()