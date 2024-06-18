# 亮点：对周的处理
from datetime import datetime
import os
from tempfile import NamedTemporaryFile # 临时文件
from jinja2 import Environment, FileSystemLoader

# 本地包
from .Utils import Utils,DateHandler


class Template:
    # 首次创建的配置文件
    config_json = {
        "global": {
            "create_at": "",    # 创建日期
            "last_modify": "",  # 最后修改日期
            "work_day": -1,     # 
            "work_week": -1,
        },
        "detail": [],
    }
    
    config_week_detail = {
        "name": "week1",
        "desc": "系统创建-首周",
        "date": [], # 本周的所有天
        "detail":[] # 本周的每一天的情况[里面有多个detail]
    }
    
    config_day_detail = {
        "date": "month-day",
        "work_day": 1,
        "work_week": 1,
        "work_brief": "work_brief_default",
        "work_list": "work_list_default",
        "work_todo": "work_todo_default",
        "work_content": "work_content_default",
        "work_link": "work_link_default",
    }
    
    # 周报模板数据
    weekly_template_vars={
        "week": "week_default",
        "day": "date_default",
        "type": "type_default",
        "ip": 1,
        "curr_date": "curr_date",
        "curr_date_badage": "curr_date_badage",
        "work_list": "work_list",
        "work_detail": "work_detail",
        "work_summary": "work_summary",
        
        "weekly_plan":"default",
        "weekly_content":"weekly_content",
        "weekly_summary":"weekly_summary",
        "weekly_report_data":[{
            "date":"default",
            "content":"default",
            "class":"default",
            "link":"default"
        }]
    }
    
    # 日报模板数据
    daily_template_vars = {
        "week": "week_default",
        "day": "date_default",
        "type": "type_default",
        "ip": 1,
        "curr_date": "curr_date",
        "curr_date_badage": "curr_date_badage",
        "work_list": "work_list",
        "work_detail": "work_detail",
        "work_summary": "work_summary",
        
        "work_brief":"work_brief",
        "work_class":"work_class",
       " work_link":"work_link"
    }
    
    header = """
<h1 align="center"> CanWay工作日志 </h1>
<div align="center">
    <img src="https://static.cwoa.net/d7c920db68254e858dc40e9064a8d4b2.png" style="width:250px;" /><br>
    <p align="center">
    <strong>简体中文</strong> | <a href="">English</a>
    </p>
    <a href ="http://10.10.41.235:8000/"><img src="https://img.shields.io/badge/Blog-dancehole-orange?style=flat&logo=microdotblog&logoColor=white&labelColor=blue"></a>
    <a href ="https://gitee.com/dancehole"><img src="https://img.shields.io/badge/Gitee-dancehole-orange?style=flat&logo=gitee&logoColor=red&labelColor=white"></a>
    <a href ="https://github.com/dancehole"><img src="https://img.shields.io/badge/Github-dancehole-orange?style=flat&logo=github&logoColor=white&labelColor=grey"></a>
</div>

<div align="center">
    <a><img src="https://img.shields.io/badge/入职嘉为-第{{week}}周-yellow"></a>
    <a><img src="https://img.shields.io/badge/累计工作-第{{day}}天-blue"></a>
    <a><img src="https://img.shields.io/badge/{{curr_date_badage}}-工作{{type}}报-green"></a>
</div>

<p align="center" style="border: 1px solid black; padding: 5px; margin: 10px 0;">
    <b>{{curr_date}}嘉为实习{{type}}报CanLab</b><br>邓仕昊#(sx_dancehole@Canway.net)<br>欢迎访问日报源网址<a href="{{ip}}">{{ip}}</a>
    </p>
    """

    content = """
## 1. 今日工作概要

{{work_list}}

## 2. 工作内容记录

{{work_detail}}

## 3. 总结与思考

{{work_summary}}

    """
    
    content_weekly = """
## 1. 本周工作总结
{{weekly_summary}}
## 2. 问题总结与解决思路
{{weekly_content}}
## 3. 下周工作计划
{{weekly_plan}}
    """

    footer = """
## 附录

| 日期  | 工作主要内容 | 所在项目分类 | 文章输出 |
| ----- | ---------- | --------- | -------- |
| 第{{week}}周 | 第{{day}}天   |      |          |
|  {{curr_date}}     |      {{work_brief}}   |    {{work_class}}|  {{work_link}}|

我的工作日报已经公开，支持每日日报的查看。**更详细的工作日报输出和文档流输出，请[访问这里]({{ip}})。**

"""

    weekly_footer = """
## 附录
### 工作日志摘要
|日期 | 工作主要内容 | 所在项目/分类 | 工作日报链接 |
|---|---|---|---|
{%for index in weekly_report_data%}| {{index.date}} | {{index.content}} |{{index.class}} |{{index.link}} |
{%endfor%}
"""

    default_work_list = """
### 1.1 工作安排
1. (default)完成第一个工作
2. (default)完成第二个工作
3. (default)完成第三个工作

### 1.2 时间安排
1. 9:00-12:00---工作一
2. 14:00-16:00---工作二
3. 16:00-18:00---工作三

    """
    
    default_work_detail = """
> 遇到问题，解决问题并记录，方便积累与复用

### 2.1 工作一
**第一个方面遇到的问题**
**解决方案**
### 2.2 工作二
**第二个方面遇到的问题**
**解决方案**

    """
    
    
    default_work_summary = """
### 3.1 今日未完成工作【暨明日todo】
1. (default)第一个工作
2. (default)第二个工作
3. (default)第三个工作
    
### 3.2 今日总结
1. (default)总结1
2. (default)总结2
    """


    """渲染模板
    @prop:fill_data:填充数据
    @prop:output_path:文件路径 接收一个或者两个参数
    返回值:true 成功/失败
    
    注意：默认模板文件在Common目录下(base_directory)
    """
    @staticmethod
    def render_template(fill_data, *args):
        output_path = args[0] if len(args) == 1 else os.path.join(args[0],args[1])
        # 加载模板文件[自动识别周报或者日报]
        str = Template.header+Template.content+Template.footer if fill_data["type"]=="日" else Template.header+Template.content_weekly+Template.weekly_footer
        env = Environment()
        try:
            # 渲染模板
            rendered_markdown = env.from_string(str).render(fill_data)
            # 输出渲染后的Markdown
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered_markdown)
            return True
        except Exception as e:
            # logging.error(e)
            return False
        
    """创建缺省的config模板,传入配置文件路径
    Returns:
        Dict: 返回配置的字典
    """
    @staticmethod
    def create_default_config(arg_date):
        config = Template.config_json
        # 稍微初始化一下子
        format_date = arg_date.strftime("%m-%d")
        # global
        config["global"]["create_at"] = format_date
        config["global"]["last_modify"] = format_date
        config["global"]["work_day"] = 1
        config["global"]["work_week"] = 1
        # 添加第一周
        config["detail"].append(Template.config_week_detail)
        config["detail"][0]["date"].append(format_date)
        # 第一天
        config["detail"][0]["detail"].append(Template.config_day_detail)
        config["detail"][0]["detail"][0]["date"] = format_date
        
        return config
    
    """创建新的一周config（硬计算，不依赖配置文件）+ 校验是否要生成
    params:
        arg_date: datetime
        config: Dict(既要读取也要修改)
    """
    @staticmethod
    def create_weekly_config(arg_date,config):
        offset = DateHandler.get_date_offsets(config,arg_date)

        # 检查week是否已经存在
        if(len(config["detail"])==offset["offset_weeks"]):
            print("本周config已存在，不需要新增")
        else:
            print("新增本周config")
            config["detail"].append(Template.config_week_detail)
            config["detail"][offset["offset_weeks"]-1]["name"] ="week"+str(offset["offset_weeks"])
        return config
        
    
    """更新某一天的config
    statement:
        1. 检查是否需要新增周config
        2. 检查是否需要新增dayconfig
    params:
        arg_date: datetime
        config: Dict(既要读取也要修改)
    """
    @staticmethod
    def update_daily_config(arg_date,config):
        offset = DateHandler.get_date_offsets(config,arg_date)
        date_formate = arg_date.strftime("%m-%d")
        __offset_week = offset["offset_weeks"]-1
        

        
        # 判断是否需要建立新的一周
        if len(config["detail"]) < offset["offset_weeks"]:
            config = Template.create_weekly_config(arg_date,config)
            
        # 检查day是否已经存在
        for i in config["detail"][__offset_week]["date"]:
            if i==date_formate:
                print("config的该日期已经存在")
                return config
        else:
            print("新增本日config")
            # 修改global
            config["global"]["last_modify"] = date_formate
            config["global"]["work_day"] += 1
            # 修改detail
            __day_template = Template.config_day_detail
            __day_template["date"] = date_formate
            __day_template["work_day"] = offset["offset_days"]
            # 修改week_config
            config["detail"][__offset_week]["date"].append(date_formate)
            config["detail"][__offset_week]["detail"].append(__day_template)
        return config
            
        

    
"""增加一个测试接口"""
def test_render_template():
    # 使用当前时间作为模拟数据的一部分，以确保每次测试都有不同的日期信息
    now = datetime.now()
    test_data = {
        "week": 1,  # 示例：假设是下周
        "day":  1,    # 示例：假设是明天
        "type": "日",
        "curr_date": now.strftime("%m-%d"),# 当前日期格式化
        "curr_date_badage": now.strftime("%m--%d"),
        "work_brief": 'default',
        "work_list": Template.default_work_list,
        "work_detail": Template.default_work_detail,
        "work_summary":Template.default_work_summary,
        "work_class": "default",
        "work_link": "http://10.10.41.235:8001/",   # 日报的链接地址，细化
        "ip": "http://10.10.41.235:8001/",  # 示例IP地址
    }
    test_weekly_data = {
        "week": 1,  # 示例：假设是下周
        "day":  1,    # 示例：假设是明天
        "type": "周",
        "curr_date": now.strftime("%m-%d"),# 当前日期格式化
        "curr_date_badage": now.strftime("%m--%d"),
        "work_list": Template.default_work_list,
        "work_detail": Template.default_work_detail,
        "work_summary":Template.default_work_summary,
        "ip": "http://10.10.41.235:8001/",  # 示例IP地址
        "weekly_plan":"default",
        "weekly_summary":"default",
        "weekly_content":"default",
        "weekly_report_data":[
            {
                "date":"2023-05-01",
                "content":"defaultcontent",
                "class":"defaultclass",
                "link":"defaultlink"
            },
            {
                "date":"2023-05-02",
                "content":"defaultcontent",
                "class":"defaultclass",
                "link":"defaultlink"
            }
        ]
    }

    # 使用临时文件进行测试，避免污染实际文件系统
    with NamedTemporaryFile(mode="w+", suffix=".md", delete=False) as temp_file:
        output_path = temp_file.name
        success = Template.render_template(test_data, output_path)
    if success:
        print(f"测试渲染日报成功，输出文件位于：{output_path}")
    else:
        print("测试渲染失败")
        
    # 使用临时文件进行测试，避免污染实际文件系统
    with NamedTemporaryFile(mode="w+", suffix=".md", delete=False) as temp_file:
        output_path = temp_file.name
        success = Template.render_template(test_weekly_data, output_path)
    if success:
        print(f"测试渲染周报成功，输出文件位于：{output_path}")
    else:
        print("测试渲染失败")
        
    # 可选：返回或打印渲染状态，以及可能的错误信息
    return success
        
        
def main():
    # 测试接口
    test_render_template()
    
# 如果脚本直接运行，执行main函数
if __name__ == "__main__":
    main()
