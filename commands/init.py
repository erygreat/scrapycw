import sys

from scrapycw.commands import ScrapycwCommand
from scrapycw.django_manage import main


class Command(ScrapycwCommand):

    can_print_result = False

    def run(self, args, opts):
        print("=========== 开始初始化 ===========")
        print("==== 创建数据库表 ===")
        sys.argv = ['django_manage.py', 'migrate']
        main()
        print("=========== 初始化完成 ===========")

    def short_desc(self):
        return "List of project"

    def long_desc(self):
        return "List of project"
