from problem.models import Problem
from utils.dockerController import DockerController
from utils.flag import generate_flag_command
import time


def refresh_flag():
    docker_controller = DockerController()

    problems = Problem.objects.all()
    for problem in problems:
        problem.flag, command = generate_flag_command(problem.template.change_flag_command)
        docker_controller.exec_container(problem.container_id, command)
        problem.rounds = problem.rounds + 1
        problem.status = 'running'
        problem.save()
        check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{check_time}  ROUNDS {{{problem.rounds}}} {problem.container_id} flag update {problem.flag}")
