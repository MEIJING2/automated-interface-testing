import os
import sys

# 这段代码会把项目根目录添加到Python的模块搜索路径中，让Python可以找到utils目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))