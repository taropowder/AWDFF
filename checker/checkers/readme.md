# checker编写指南
例子

```python
from checker.checker import CheckerTemplate, ProblemTemplate


class dvwaCheck(CheckerTemplate):
    checker_problem_template = ProblemTemplate.objects.get(image_id='b843afe11c5f')

    def _prepare(self):
        return True

    def _check1(self):
        # print('check1')
        return False, 'reason'
```

## 所有的checker继承自 `CheckerTemplate` 这个类,
- 需要实现的方法有    
    + `_prepare` 方法,用于checker脚本最初始化时调用,可用来`注册`,`登录`
    + `_check` 方法,会依次调用 `_check1()` -- `_check5()` (最多五个check逻辑),不需要全部实现
- 需要实现的类变量有
    + `checker_problem_template` 需绑定一个 `ProblemTemplate` 对象,用于判定checker对应题目
- 内部成员变量
    + `self.session` --> `request.Session 对象`
    + `self.url` --> `需要check的url`
    + `self.problem` --> `check的题目`
    
需要用到其他变量请阅读CheckerTemplate 源码

## 文件以及类命名

