import os
import sys

from scrapycw.commands import ScrapycwCommand
from scrapycw.django_manage import main
from scrapycw.settings import RUNTIME_PATH


class Command(ScrapycwCommand):

    can_print_result = True

    def syntax(self):
        return ""

    def run(self, args, opts):
        self.print("=========== 开始初始化 ===========")
        if not os.path.exists(RUNTIME_PATH):
            self.print("======= 初始化运行目录 ==========")
            os.makedirs(RUNTIME_PATH)
        self.print("==== 创建数据库表 ===")
        argv = sys.argv
        sys.argv = ['django_manage.py', 'migrate']
        main()
        sys.argv = argv
        self.print("=========== 初始化完成 ===========")

    def short_desc(self):
        return "init project, create database"

    def long_desc(self):
        return "init project, create database"

    def print(self, message):
        if self.can_print_result:
            print(message)
