# 亮点：对周的处理
class Template:
    config_json = {
        "global": {
            "create_at": "",
            "last_modify": "",
            "work_day": -1,
            "work_week": -1,
        },
        "detail": [
            {
                "name": "week1",
                "desc": "测试",
                "date": ["04-24"],
                "detail": [
                    {
                        "date": "04-24",
                        "work_day": 1,
                        "work_week": 1,
                        "work_brief": "标题/工作概要，一句话",
                        "work_list": "工作内容列表，可以是一段话,可以是昨天没干完的事情todo",
                        "work_todo": "今天没干完的事情",
                        "work_content": "工作内容",
                        "work_link": "日报链接,支持自定义",
                    }
                ]
            }
        ],
    }
    header = """
<h1 align="center"> CanWay工作日志 </h1>

<div align="center">
        <img src="https://static.cwoa.net/d7c920db68254e858dc40e9064a8d4b2.png" style="width:250px;" /><br>
    <p align="center">
    <strong>简体中文</strong> | <a href="readme_en.md">English</a>
</p>
    <a href ="http://10.10.41.235:8000/"><img src="https://img.shields.io/badge/Blog-dancehole-orange?style=flat&logo=microdotblog&logoColor=white&labelColor=blue"></a>
    <a href ="https://gitee.com/dancehole"><img src="https://img.shields.io/badge/Gitee-dancehole-orange?style=flat&logo=gitee&logoColor=red&labelColor=white"></a>
    <a href ="https://github.com/dancehole"><img src="https://img.shields.io/badge/Github-dancehole-orange?style=flat&logo=github&logoColor=white&labelColor=grey"></a>
</div>
<div align="center">
    <a><img src="https://img.shields.io/badge/入职嘉为-第{{week}}周-yellow"></a>
    <a><img src="https://img.shields.io/badge/工作日报-第{{day}}天-blue"></a>
    <a><img src="https://img.shields.io/badge/{{curr_date}}-工作{{type}}报-green">
</div>

<p align="center" style="border: 1px solid black; padding: 5px; margin: 10px 0;">
    <b>嘉为实习{{type}}报CanLab-{{date}}</b><br>邓仕昊@Canway<br><a href="{{ip}}">{{ip}}</a>
    </p>
    """
    content = """
    
## 今日工作概要

> 来自昨日todo

{{work_list}}


## 工作内容记录

> 类似于工作日志

{{work_detail}}


## 明日计划todo

> 给明天/未来做todo，没完成的自动继承，完成了自动删除

{{todo}}


## 结语

我的工作日报已经公开，支持每日日报的查看。**更详细的工作日报输出和文档流输出，请[访问这里]({{ip}})。**

- 出于安全性考虑，网站只在**内网的工作时间**部署，暂不支持导出
    """
    
    footer = """
    
## 附录

## ※工作日志摘要

> 方便填写erp

| 日期  | 工作主要内容 | 所在项目/分类 | 文章输出 |
| ----- | ------------ | ------------- | -------- |
| 第{{week}}周 | 第{{day}}天        |               |          |
|  {{curr_date}}     |      {{work_brief}}        |    {{work_class}}           |    {{work_link}}      |
"""