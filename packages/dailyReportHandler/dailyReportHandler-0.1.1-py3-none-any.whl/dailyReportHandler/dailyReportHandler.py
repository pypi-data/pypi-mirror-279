# 日报类，主要处理日报+周报处理【逻辑核心】
class DailyReportHandler:
    def __init__(self, cmd, *args, **kwargs) -> None:
        # 参数初始化
        self.parse_args(cmd, *args, **kwargs)
        # 路径初始化，支持多种路径下调用【含cmd里，含校验，或者】
        self.__init_path()
        # 读取config文件
        self.parse_config()
        # 检查daily下目录和文件是否生成
        dir_name =  self.get_weekly_dir_name()
        # 周报处理
        self.create_weekly_report(dir_name)
        # 日报处理
        self.create_daily_report(dir_name)
        # 写入config文件【最后一起写入】
        Utils.write_json(self.config,os.path.join(self.path["root"], "config.json"))

    # 参数初始化
    def parse_args(self, cmd, *args, **kwargs):
        # self.arg_action = cmd.action
        self.arg_date = cmd.date
        self.arg_path = cmd.path
        # 其他参数：暂未确定

    # 创建缺省的config,传入配置文件路径
    def create_default_config(self,config_file):
        config = Template.config_json
        # 稍微初始化一下子
        format_date = self.arg_date.strftime("%m-%d")
        config["global"]["create_at"] = format_date
        config["global"]["last_modify"] = format_date
        config["global"]["work_day"] = 1
        config["global"]["work_week"] = 1
        config["detail"][0]["date"] = [format_date]
        config["detail"][0]["detail"][0]["date"] = format_date
        config["detail"][0]["detail"][0]["work_day"]=1
        config["detail"][0]["detail"][0]["work_week"]=1
        
        Utils.write_json(config, config_file)
        return config

    # 解析config参数(如果为空，则要创建)
    def parse_config(self):
        config_file = os.path.join(self.path["root"], "config.json")
        if not os.path.exists(config_file):
            print("json文件不存在,正在创建ing")
            self.config = self.create_default_config(config_file)
        else:
            self.config = Utils.read_json(config_file)
            if self.config == None: # 检查config格式，todo
                pass
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
                print(f"切换到父级目录为{base_dir}")
                continue
            else:
                flag = True
                print(f"找到基目录为{base_dir}")
        if not flag:
            # 创建目录 直接以arg.path为基目录
            user_input = input("基目录不存在，输入y/Y创建目录")
            if(user_input in ["y","Y"]):
                print("正在创建目录")
                base_dir = self.arg_path    # 把base_dir回到参数的目录上
                for name in base_dir_list:
                    os.makedirs(os.path.join(self.arg_path, name)) if not os.path.exists(os.path.join(self.arg_path, name)) else None
            else :
                print("退出")
                exit(0)
        self.path = {
            "root": base_dir,
            "archivingFile": os.path.join(self.arg_path, "archivingFile归档文件"),
            "common": os.path.join(self.arg_path, "Common常用"),
            "dailyReport": os.path.join(self.arg_path, "dailyReport日报"),
            "docsOutput": os.path.join(self.arg_path, "docsOutput文档输出"),
        }
        pass
    
    # get_monday_of_date 获取当前日期是星期几
    def get_monday(self,date):
        days_to_monday = (date.weekday()) % 7
        return date - timedelta(days=days_to_monday)

    def get_week_offset_by_config(self):
        # 获取当前日期是星期几
        weekday = self.arg_date.weekday()
        # 获取当前日期是第几周
        week_offset = (self.arg_date.day - 1) // 7 + 1
        return week_offset
    
    # 根据arg.date结合config文件，获取当前“周数+周开始日”【同时结合计算和config文件】周的计算从入职开始
    # 优点：不上班也会计算日子和周数。缺点有时候放国庆/五一，一周可能就一天日报，，
    def get_week_offset(self):
        # 处理第一天+所在周的计算[可以计算入职天数&整周数]
        first_day = self.config["global"]["create_at"]
        # mm-dd转datetime
        first_date = datetime.strptime(f'2024-{first_day}', '%Y-%m-%d')
        first_date_offset = first_date.weekday()+1
        
        first_monday = self.get_monday(first_date)
        curr_monday  = self.get_monday(self.arg_date)
        
        print("入职日期",first_date)
        print("入职是星期",first_date_offset)
        print("入职当周开始时间是",first_monday)

        
        print("现在是",self.arg_date.strftime("%m-%d"))
        print("现在是星期",self.arg_date.weekday()+1)
        print("这周开始时间是",curr_monday)
        
        offset_days  = (self.arg_date - first_date).days+1
        offset_weeks = offset_days // 7 +1
        
        print("入职",offset_days,"天，入职第",offset_weeks,"周")

        return {
            "offset_days":offset_days,
            "offset_weeks":offset_weeks,
            "curr_monday":curr_monday.strftime("%m-%d"),
            "first_monday":first_monday
        }

    # 检查传入的日期是否创建了相应的目录（weekx）
    # 如传入04-26,要检查其在04-24-week1目录下
    def get_weekly_dir_name(self):
        offset = self.get_week_offset()
        
        week_file_name = offset["curr_monday"]+"-week"+str(offset["offset_weeks"])
        print("正在检查所在周目录：",week_file_name)
        # 检查是否存在
        if not os.path.exists(os.path.join(self.path["dailyReport"],week_file_name)):
            pass
            print("目录不存在，正在创建",week_file_name)
            os.makedirs(os.path.join(self.path["dailyReport"],week_file_name))
        else :
            print("目录已经存在")
        
        return week_file_name


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
        return filled_data

    # 更新config.json：当且仅当创建日报时，更新config.json
    def update_config(self):
        self.config["global"]["work_day"] += 1
        self.config["global"]["work_week"] = self.get_week_offset()["offset_weeks"]
        # 插入当日数据
        self.config["detail"][self.config["global"]["work_week"]-1]["date"].append(self.arg_date.strftime("%m-%d"))
        temp ={
          "date": "06-03",
          "work_day": 1,
          "work_week": 1,
          "work_brief": "brief_todo",
          "work_list": "list_todo",
          "work_todo": "todo_todo",
          "work_content": "content_todo",
          "work_link": "link_todo"
        }
        self.config["detail"][self.config["global"]["work_week"]-1]["detail"].append(temp)
        
        
    # 填充周报的模板数据，模板参考readme:weekly_test_data{date,content,class,ip}
    # 待完成
    def get_weekly_report_data(self):
        return
        week = self.get_week_offset()["offset_weeks"]
        date_list = self.config["detail"][week]["date"]
        content_list = [self.config["detail"][week]["detail"][i]["work_brief"] for i in range(len(date_list))]
        class_list = [self.config["detail"][week]["detail"][i]["class"] for i in range(len(date_list))]
        ip_list = [f"{self.ip}{date}" for date in date_list]
        
        print(date_list)
        print(content_list)
        print(ip_list)
     
    # 生成周报    
    def create_weekly_report(self,dir_name):
        # 检查是否要生成周报：每周五/六(且周报不存在)
        file_path = os.path.join(self.path["dailyReport"],dir_name,"week"+str(self.config["global"]["work_week"])+"周报.md")
        if self.arg_date.weekday() >= 4 and not os.path.exists(file_path):
            print("正在生成周报",file_path)
            fill_data = self.get_weekly_report_data()
            self.render_template(fill_data, file_path)

        # 检查是否是新的一周，要迁移common目录【未完成】
        # if self.arg_date.weekday() == 0 and self.config["global"]["work_week"] != self.get_week_offset()["offset_weeks"]:
        #     print("正在迁移common目录",self.path["dailyReport"],self.path["common"],dir_name)
        #     # 迁移common目录
        #     shutil.move(self.path["common"],os.path.join(self.path["dailyReport"],dir_name))
            
    def create_daily_report(self,dir_name):
        # 检查是否要生成日报
        file_path = os.path.join(self.path["dailyReport"],dir_name,self.arg_date.strftime("%m-%d")+".md")
        if not os.path.exists(file_path):
            print("正在生成日报",file_path)
            self.update_config()
            fill_data = self.get_daily_data()
            self.render_template(fill_data, file_path)
            
        pass
    
    """渲染模板
    @prop:fill_data:填充数据
    @prop:output_path:文件路径 接收一个或者两个参数
    返回值:true 成功/失败
    
    注意：默认模板文件在Common目录下(base_directory)
    """
    def render_template(self, fill_data, *args):
        output_path = args[0] if len(args) == 1 else os.path.join(args[0],args[1])
        # 加载模板文件
        str = Template.header+Template.content+Template.footer
        env = Environment()
        try:
            # 渲染模板
            rendered_markdown = env.from_string(str).render(fill_data)
            # 输出渲染后的Markdown
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered_markdown)
            return True
        except Exception as e:
            logging.error(e)
            return False
