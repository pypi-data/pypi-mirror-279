from setuptools import setup, find_packages

# 打包过程：
# 1. 打包：python setup.py sdist bdist_wheel
# 2. 上传：twine upload dist/*
# 本地安装：pip install ./dailyReportHandler-1.0.0.whl
# 或者tar.gz
# 安装完成后就可以随地大小便了

# 0.1.0 更新：完成安装包流程
# 0.1.1 更新：测试命令行调用
# 0.1.2 更新：可以正确解析命令行参数+过整体流程
# 1.0   更新：完善所有功能，可以正常生成日报周报，处理模板等（开箱即用）
# 1.0.1 更新：修改导入包失败的bug

setup(
    name='dailyReportHandler',  # 包名
    version='1.0.0',    # 版本号
    packages=find_packages(),  # 自动发现所有包
    install_requires=['requests'],  # 依赖列表
    author='Dancehole',  # 作者名
    author_email='1391755954@qq.com',  # 作者邮箱
    description='A file manager to generate daily report',  # 包描述
    long_description=open('readme.md',encoding="utf-8").read(),  # 详细描述，可读取README文件
    long_description_content_type='text/markdown',  # README文件类型，如果是Markdown
    url='https://github.com/dancehole/dailyReportHandler',  # 项目URL
    classifiers=[  # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # 程序入口点[命令行]
    entry_points={
        'console_scripts': [
            'daily=dailyReportHandler.cmd:main',
        ]
    }
)
