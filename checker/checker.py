import requests
from problem.models import Problem, ProblemTemplate, Down
from utils.dockerController import DockerController
from utils.flag import generate_flag_command


class CheckerTemplate:
    docker_controller = DockerController()

    # checker_problem_template = ProblemTemplate.objects.get(image_id='xxxxxx')

    def __init__(self, problem: Problem):
        # TODO 改为可配置
        self.problem = problem
        self.ip = '127.0.0.1'
        self.protocol = 'http'
        self.port = problem.web_external_port
        self.session = requests.Session()
        self.url = f"{self.protocol}://{self.ip}:{self.port}/"
        try:
            self._prepare()
        except Exception as e:
            pass
        self.result = {}

    @classmethod
    def check_or_die(cls, problem: Problem):
        if problem.template == cls.checker_problem_template:
            return cls(problem)
        else:
            return False

    def _prepare(self):
        return True

    def check(self):
        # TODO 读取类中_check函数的个数,自动调用
        self.result['status'] = True
        for i in range(1, 5):
            try:
                checker = getattr(self, '_check' + str(i))
            except AttributeError:
                break
            try:
                res = checker()
            except Exception as e:
                res = [False, e]
            if not res[0]:
                self.result['status'] = False
                self.result['reason'] = res[1]
                break
        # if checker:
        #     print(checker)
        # if self._check1() and self._check2():
        #     self.result['status'] = True
        # else:
        #     self.result['status'] = False
        #     self.result['reason'] = '0xff'

        return self.result

    def _check1(self):
        # return False, 'reason'
        return True, 'ok'

    def __del__(self):
        if not self.result['status']:
            self.problem.status = 'down'
            self.problem.save()
            try:
                down = Down.objects.get(team=self.problem.team, rounds=self.problem.rounds)
            except Down.DoesNotExist:
                down = None
            if not down:
                Down.objects.create(team=self.problem.team, rounds=self.problem.rounds, problem=self.problem)
        # self.problem.flag, command = generate_flag_command(self.problem.template.change_flag_command)
        # self.docker_controller.exec_container(self.problem.container_id, command)


if __name__ == '__main__':
    c = CheckerTemplate()
    c.check()
