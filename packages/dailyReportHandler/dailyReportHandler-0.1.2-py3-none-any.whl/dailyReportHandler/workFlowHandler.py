"""已弃用

Returns:
    _type_: _description_
"""


# 工作流处理类，包含日报处理，目录处理
class WorkFlowHandler:
    def __init__(self, args):
        self.args = args
        # 路径初始化
        self.__init_path()

        # 日志配置
        self.__init_logger()
        logging.info(f'初始化完成,正在生成{args.date.strftime("%m-%d")}的日报')

        # 日期初始化
        # self.__init_date(args)
        self.week_offset = 1

        # 日报目录初始化
        self.__init_daily_report_dir()

        # 日报或者周报处理
        # self.__init_daily_report()
        self.create_daily_report()

    def __init_path(self):
        # 这里的路径会经常有问题，不同环境下的问题/不同情况调用的问题。所以使用os.path.dirname(__file__)获取文件当前目录（应该会在Common下）
        self.PATH = {
            "base_directory": os.path.dirname(
                __file__
            ),  # 基础目录(设python所在目录)，可以根据需要更改，防止bash影响
        }
        self.PATH["root_directory"] = os.path.dirname(self.PATH["base_directory"])

        self.PATH["daily_report_directory"] = os.path.join(
            self.PATH["root_directory"], "dailyReport日报"
        )
        # self.PATH["daily_report_directory"] = os.path.join(self.PATH["root_directory"], "@override")

        self.PATH["daily_report_directory_dst"] = self.PATH[
            "daily_report_directory"
        ]  # 需要初始化
        self.PATH["common_directory"] = os.path.join(
            self.PATH["root_directory"], "Common常用"
        )
        self.PATH["log_path"] = os.path.join(self.PATH["common_directory"], "daily.log")

    def __init_date(self, args):
        dst_date = args.date if args.date else datetime.now().strftime("%m-%d")
        # 转换为datetime对象
        date_object = datetime.strptime(dst_date + "-2024", "%m-%d-%Y")
        self.DATE = {
            "date_now": date_object,  # 存储当前日期时间对象
        }
        # 使用字典中的date_now来获取日期时间对象
        self.DATE.update(
            {
                "date_format": self.DATE["date_now"].strftime("%Y-%m-%d"),
                "date_format2": self.DATE["date_now"].strftime("%m-%d"),
                "year": self.DATE["date_now"].year,
                "month": self.DATE["date_now"].month,
                "day": self.DATE["date_now"].day,
                "week": self.DATE["date_now"].isocalendar()[1],
                "weekday": self.DATE["date_now"].isocalendar()[2],
            }
        )
        print("初始化目录：", self.PATH)
        print("初始化日期：", self.DATE)

    # 根据传入的参数，判断对应日期的创建日报目录
    def __init_daily_report_dir(self):

        self.args = self.args.date  # 类型是datetime
        # 获取所有子目录名称，并分割为[['04', '24', 'week1', '入职'], ['05', '06', 'week2', '五一后', 'zbank']]
        subdirs = tuple(
            d
            for d in os.listdir(self.PATH["daily_report_directory"])
            if os.path.isdir(os.path.join(self.PATH["daily_report_directory"], d))
        )
        split_subdirs = []
        for item in subdirs:
            split_dir = item.split("-")
            split_subdirs.append(split_dir)
        # print("分割后的daily目录：",split_subdirs)

        # 如果整个目录为空，则直接新建第一周
        if not subdirs:
            week1_path = os.path.join(
                self.PATH["daily_report_directory"],
                self.args.strftime("%m-%d") + "-week1",
            )
            os.mkdir(week1_path)
            logging.info("创建第一周的目录：" + week1_path)
            self.PATH["daily_report_directory_dst"] = os.path.join(
                self.PATH["daily_report_directory_dst"], week1_path
            )
            return
        # 目录不为空，则获取基准日期和周数
        else:
            first_week = split_subdirs[0][2]
            first_month = split_subdirs[0][0]
            first_day = split_subdirs[0][1]
            first_date = datetime(2024, int(first_month), int(first_day))

            # 获取当前日期的周数
            args_monday = (
                self.args
                if self.args.weekday() == 0
                else self.args - timedelta(days=self.args.weekday())
            )
            # logging.info("当周开始日期为",args_monday)
            # 获取week
            delta_days = (args_monday - first_date).days
            # 转换为整周数，向下取整
            weeks_between = delta_days // 7
            self.week_offset = weeks_between + 1

        # 判断是否在任意一个目录下
        need_to_create_flag = True
        for subdir in split_subdirs:
            if (
                len(subdir) >= 3
                and (int(subdir[0]) == self.args.month)
                and (self.args.day - int(subdir[1]) <= 6)
            ):
                logging.info(
                    f"{self.args} 属于 {subdir[0]}-{subdir[1]}-{subdir[2]} 目录"
                )
                self.PATH["daily_report_directory_dst"] = os.path.join(
                    self.PATH["daily_report_directory_dst"],
                    f"{subdir[0]}-{subdir[1]}-{subdir[2]}",
                )
                need_to_create_flag = False
                break
        # 假如不满足，则要新建目录
        if need_to_create_flag:
            # 构建目录-日期(周开始日期-周数)
            logging.info(f"{self.args} 不属于任何已知目录,正在新建ing")

            dir_name = (
                f"{args_monday.month:02d}-{args_monday.day:02d}-week{weeks_between+1}"
            )
            logging.info("这是第", weeks_between + 1, "周，正在建立目录名 : ", dir_name)
            self.PATH["daily_report_directory_dst"] = os.path.join(
                self.PATH["daily_report_directory_dst"], dir_name
            )

            # 新建工作流文件
            work_dir = os.path.join(self.PATH["daily_report_directory"], dir_name)
            logging.info("新建目录 : ", work_dir)
            os.mkdir(work_dir)

        print("更新工作目录为", self.PATH["daily_report_directory_dst"])
        os.chdir(self.PATH["daily_report_directory_dst"])
        return

    def __init_logger(self):
        # 设置日志配置
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] - [%(levelname)s] - [%(message)s]",
            datefmt="%Y-%m-%d %H:%M",  # 时间格式精确到分钟，不要秒和毫秒
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(
                    self.PATH["common_directory"] + "/daily.log",
                    mode="a",
                    encoding="utf-8",
                ),
            ],
        )

    def test(self):
        pass

    # 读取json文件，并返回一个字典
    def read_config(self):
        with open(self.PATH["common_directory"] + "/config.json", "r") as file:
            file_content = file.read()
            if file_content == "":
                return None

        # 解析JSON数据
        parsed_data = json.loads(file_content)
        return parsed_data  # 返回解析后的数据

    def write_config(self, config):
        with open(self.PATH["common_directory"] + "/config.json", "w") as file:
            data = {
                "create_at": config["create_at"],
                "last_modify": config["last_modify"],
                "work_day": config["work_day"],
                "work_week": config["work_week"],
            }
            json.dump(data, file, indent=4)
            print("写入成功")
        return True

    # 更改逻辑：弃用！弃用！
    # 生成日报或者周报 模板引擎
    def __init_daily_report(self):
        # 读取数据，由模板生成日报
        # 假如log没东西，则为第一周第一天，假如有，则继承
        message_from_log = self.get_msg_from_log()  # log里存放了工作的天数/周数
        filled_data = {}
        print(message_from_log)
        if message_from_log is None:
            filled_data = {
                "day": 1,
                "week": 1,
                "message": "系统自动生成工作第一天日志",
                "type": "日",
                "ip": "http://10.10.41.235:8001/",
                "curr_date": self.args.strftime("%Y-%m-%d"),
            }
        else:
            # todo:在任意日期读写
            # 因为涉及到读log，log的message设置为json格式（方便）
            filled_data = {
                "day": message_from_log["day"] + 1,
                "week": self.week_offset,
                "message": "创建日志的日期为" + self.args.strftime("%m-%d"),
                "type": "日",
                "ip": "http://10.10.41.235:8001/",
                "curr_date": self.args.strftime("%m-%d"),
            }

        file_name = self.args.strftime("%m-%d") + ".md"
        file_path = os.path.join(self.PATH["daily_report_directory_dst"], file_name)
        if os.path.exists(file_name):
            logging.info("工作日志已存在,创建文件失败")
            return
        else:
            logging.info("文件不存在，正在生成")
            # 写入字典
            logging.error(filled_data)
            with open(file_name, "w", encoding="utf-8") as f:

                # 继续获取模板数据，比如todo等等
                self.render_template(filled_data, file_path)
                # 假如今天是周五 生成一周周报

                return

    def create_daily_dir(self):
        pass

    # 从config中获取需要填充的数据;日报数据里的变量可以参考readme
    def get_daily_data(self):
        # 初始化一个数据结构，缺省值
        filled_data = {
            "day": 1,
            "week": 1,
            "type": "日",
            "ip": "http://10.10.41.235:8001/",
            "curr_date": self.args.strftime("%Y-%m-%d"),
        }
        new_config = self.read_config()
        if new_config is not None:
            filled_data["day"] = new_config["global"]["work_day"]
            filled_data["week"] = new_config["global"]["work_week"]
        return filled_data

    def create_daily_report(self):
        filled_data = {}
        new_config = self.read_config()
        if new_config is None:
            new_config = {
                "work_day": 1,
                "work_week": 1,
                "create_at": self.args.strftime("%m-%d"),
                "last_modify": self.args.strftime("%m-%d"),
            }
            self.write_config(new_config)
        else:
            # todo:在任意日期读写
            new_config = {
                "work_day": new_config["work_day"] + 1,
                "work_week": self.calculate_date_between(
                    new_config["create_at"], self.args.strftime("%m-%d")
                )["week"]
                + 1,
                "create_at": new_config["create_at"],
                "last_modify": self.args.strftime("%m-%d"),
            }
            self.write_config(new_config)

        filled_data = {
            "day": new_config["work_day"],
            "week": new_config["work_week"],
            "message": "创建日志的日期为" + self.args.strftime("%m-%d"),
            "type": "日",
            "ip": "http://10.10.41.235:8001/",
            "curr_date": self.args.strftime("%m-%d"),
        }
        file_name = self.args.strftime("%m-%d") + ".md"
        file_path = os.path.join(self.PATH["daily_report_directory_dst"], file_name)
        if os.path.exists(file_name):
            logging.info("工作日志已存在,创建文件失败")
            return
        else:
            logging.info("文件不存在，正在生成")
            # 写入字典
            logging.error(filled_data)
            # 继续获取模板数据，比如todo等等
            self.render_template(filled_data, file_path)
            # 假如今天是周五 生成一周周报
            pass
        return

    def create_weekly_report(self):
        pass

    # 生成工作流目录 方便移植 todo未完成
    def init_dir(self):
        directories = [
            "archivingFile",
            "Common",
            "dailyReport",
            "docsOutput",
        ]

        for dir_path in directories:
            dir_path = dir_path.replace(" ", "").replace("(", "").replace(")", "")
            dir_path = dir_path.replace("---", "_").replace("--", "-")
            full_path = os.path.join("root_directory", dir_path)
            os.makedirs(full_path, exist_ok=True)

    # 找到log里的最后的info/ERROR 行，并读取日期信息
    def get_msg_from_log(self, log_level="ERROR"):
        with open(self.PATH["log_path"], "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_info_line = None
            for line in reversed(lines):
                if f"[{log_level}]" in line:
                    last_info_line = line
                    break

        if last_info_line is not None:
            print("NOT NONE")
            # 使用正则表达式提取字典部分
            match = re.search(rf"\[.*\] - \[{log_level}\] - \[(.*)\]", last_info_line)
            if match:
                dict_str = match.group(1)

                # 将字符串解析为字典
                data_dict = eval(dict_str)
                return data_dict
        return None

    """渲染模板
    @prop:fill_data:填充数据
    @prop:output_path:文件路径
    返回值:true 成功/失败
    
    注意：默认模板文件在Common目录下(base_directory)
    """

    def render_template(self, fill_data, output_path, template_name):

        # 加载模板文件
        loader = FileSystemLoader(
            self.PATH["base_directory"]
        )  # 设定相对路径为.(common)
        env = Environment(loader=loader)
        # 使用模板引擎处理md模板并渲染
        # 加载模板
        try:
            template = env.get_template(template_name)
            # 渲染模板
            rendered_markdown = template.render(fill_data)
            # 输出渲染后的Markdown
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered_markdown)
            return True
        except Exception as e:
            logging.error(e)
            return False

    """计算相隔日期
    ps:已弃用;因为日期始终算不准，不如每调用一次就创建一天(读写数据库)
    计算yyyy-mm-dd距离yyyy-mm-dd(缺省为今天)的日期差，星期差，用于计算相隔x周x月x日等
    Args:
        current_date (String:%Y-%m-%d): 当前日期
        target_date (String:%Y-%m-%d): 目标日期(缺省为04-24)
    Returns:
        Object: 'code':True/False,
                'day':相距天数,
                'week':相距周数(整周),
                'offset':偏移天数
    """

    def calculate_date_between(self, first_date, last_date="04-24"):
        try:
            # 解析日期字符串 为datetime
            first_date = datetime.strptime(first_date, "%m-%d")
            last_date = datetime.strptime(last_date, "%m-%d")

            # 计算日期差
            days_diff = (last_date - first_date).days

            # 计算周数
            weeks_diff = days_diff // 7
            remaining_days = days_diff % 7

            result = {
                "code": "True",
                "day": days_diff,
                "week": weeks_diff,
                "offset": remaining_days,
            }

            return result
        except ValueError:
            return "{'code':'False'}"

    def create_date_directories(self, currday):
        """
        根据给定的日期字符串创建文件夹+填充文件。

        参数:
            date_string (str): 格式为'YYYY-MM-DD'的日期字符串。
        """
        if not currday or not self._is_valid_date(currday):
            currday = datetime.today().strftime("%Y-%m-%d")
        firstday = "2024-04-24"

        # 获取间隔日期
        date_between = self.calculate_date_between(firstday, currday)
        # date_between.week+=1
        print(date_between)

        # year, month, day = map(int, date_string.split("-"))
        # year_folder = os.path.join(self.base_directory, str(year))
        # month_folder = os.path.join(year_folder, str(month).zfill(2))
        # day_folder = os.path.join(month_folder, str(day).zfill(2))

        # for folder in [year_folder, month_folder, day_folder]:
        #     if not os.path.exists(folder):
        #         try:
        #             os.makedirs(folder, exist_ok=True)
        #             print("ok")
        #         except Exception as e:
        #             print(e)
