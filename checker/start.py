# from checker.checkers.dvwaCheck import dvwaCheck
import importlib
import os
import time
from problem.models import Problem


def get_filename():
    script_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'checkers')
    for file in os.listdir(script_dir):
        if file.endswith('.py') and file != '__init__.py':
            yield file


def check():
    module_name = "checker.checkers"
    for file in get_filename():
        class_name = file.replace('.py', '')
        module_name = f"{module_name}.{class_name}"
        check_module = importlib.import_module(module_name)
        # 使用getattr()获取模块中的类
        check_class = getattr(check_module, class_name)
        problems = Problem.objects.all()
        for problem in problems:
            checker = check_class.check_or_die(problem)
            if checker:
                result = checker.check()
                check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                url = checker.url
                print(f"{check_time}  {url}  is {result}")


if __name__ == '__main__':
    check()
    # print(get_filename())
    # for i in get_filename():
    #     print(i)
