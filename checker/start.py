from checker.checkers.dvwaCheck import dvwaCheck
import importlib


def check():
    module_name = "checker.checkers.dvwaCheck"
    class_name = "dvwaCheck"
    test_module = importlib.import_module(module_name)
    # 使用getattr()获取模块中的类
    test_class = getattr(test_module, class_name)
    # 动态加载类test_class生成类对象
    test_obj = test_class()
    test_obj.test()


if __name__ == '__main__':
    check()
