"""
工具类，含文件读写等操作
"""
class Utils:
    # 读取json文件，并返回一个字典
    # 可以接收1个参数（文件路径）或者两个参数（路径，文件名）
    @staticmethod
    def read_json(*args, **kwargs) -> Optional[Dict[str, Any]]:
        file_name = args[0] if len(args)==1 else os.path.join(args[0], args[1])
        with open(file_name, "r", encoding="utf-8") as file:
            file_content = file.read()
            if file_content == "":
                return None

        # 解析JSON数据
        parsed_data = json.loads(file_content)
        return parsed_data  # 返回解析后的数据

    # 读取一个字典，并写入到json文件
    # 可以接收1个参数（文件路径）或者两个参数（路径，文件名）
    @staticmethod
    def write_json(json_data: Dict[Any,Any], *args) -> bool:
        file_name = args[0] if len(args)==1 else os.path.join(args[0], args[1])
        with open(file_name, "w",encoding="utf-8") as file:
            json.dump(json_data, file)
            print("写入json成功")
        return True

    @staticmethod
    def validate_path(path: str) -> str:
        # 检查路径是否为字符串
        if not isinstance(path, str):
            return False

        # 检查路径是否为绝对路径
        if not os.path.isabs(path):
            print("路径不是绝对路径")
            return False

        # 检查路径是否为文件或目录
        if not (os.path.isfile(path) or os.path.isdir(path)):
            return False

        # 检查路径是否包含非法字符（这里仅针对Windows系统）
        # if os.name == 'nt':
        #     illegal_chars = '<>:"/\\|?*'
        #     for char in path:
        #         if char in illegal_chars:
        #             print("路径包含非法字符")
        #             return False

        # 如果通过所有检查，路径是合法的
        return True


"""
处理日期类,用于检测日期合法性，生成格式化日期
应当是一个静态类
"""
class DateHandler:
    def __init__(self):
        pass

    # 检查输入日期的合法性，并转化为datetime对象
    def validate_date(date_string):
        print("---正在解析日期为", date_string, "----")
        if date_string is None or date_string == "":
            return None
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%m-%d", "%m/%d", "%m.%d"):
            try:
                date_obj = datetime.strptime("2024-" + date_string, fmt)
                # 检查月份是否大于12
                if date_obj.month > 12:
                    return None
                # 检查日期是否超过月份的最大日期
                max_days_in_month = calendar.monthrange(date_obj.year, date_obj.month)[
                    1
                ]
                if date_obj.day > max_days_in_month:
                    return None
                return date_obj
            except ValueError:
                continue
        return None

    """
    获取某天是星期几,返回列表[7, 'Sunday', '星期日']
    """

    @staticmethod
    def get_offset_of_week(date_string):
        # 解析日期字符串
        month, day = map(int, date_string.split("-"))
        date = datetime(
            2024, month, day
        )  # 假设年份是2024年，如果不确定年份，需要从其他地方获取或指定

        # 获取星期几的整数表示
        weekday_int = date.weekday()

        WEEKDAY_NAMES = [
            [1, "Monday", "星期一"],
            [2, "Tuesday", "星期二"],
            [3, "Wednesday", "星期三"],
            [4, "Thursday", "星期四"],
            [5, "Friday", "星期五"],
            [6, "Saturday", "星期六"],
            [7, "Sunday", "星期日"],
        ]
        return WEEKDAY_NAMES[weekday_int]
