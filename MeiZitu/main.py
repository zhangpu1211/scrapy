from scrapy.cmdline import execute

import sys
import os

# 将项目根目录加入系统环境变量中。
# os.path.abspath(__file__)为当前文件所在绝对路径
# os.path.dirname() 获取文件的父目录。
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl" , "image"])