from docker import DockerClient, APIClient
from utils.network import get_no_port_being_used
import logging


# from docker import Client


class DockerController:
    def __init__(self):
        self.client = DockerClient(base_url='tcp://127.0.0.1:2375')

    def _info(self):
        print(self.client.info())

    def show_running_containers(self):
        return self.client.containers.list()

    def build_image(self, path, tag):
        # path = os.path.join(os.getcwd(), 'files', dir_name)
        self.client.build(path=path, tag=tag)

    def show_images(self):
        return self.client.images()

    def run_container(self, image: str, internal_web_port: int, build_name=None, command=None):
        ssh_port = get_no_port_being_used()
        web_port = get_no_port_being_used()
        container = self.client.containers.run(image=image,
                                               ports={'22/tcp': ssh_port, f'{internal_web_port}/tcp': web_port},
                                               name=build_name, command=command, detach=True)
        logging.log(logging.INFO, f"ssh port is {ssh_port}, web port is {web_port}")
        container_info = {}
        container_info['id'] = container.id
        container_info['ssh_port'] = ssh_port
        container_info['web_port'] = web_port

        return container_info

    def rm_container(self, container_id: str):
        container = self.client.containers.get(container_id)
        # container.stop()
        # 直接删除
        container.remove(force=True)
        logging.log(logging.INFO, f'{container.id} has been removed')

    def exec_container(self, container_id: str, command):
        self.client.containers.get(container_id).exec_run(command)


if __name__ == '__main__':
    d = DockerController()
    # d.run_container('94c8d3f00904', 80)
    # d.show_running_containers()
    # d.rm_container('01eb037b8e')
    command = """ bash -c "useradd -p `openssl passwd -1 -salt 'taro' {password}` user5" """
    from utils import flag
    command = flag.generate_ssh_paasword(command)
    print(command)
    d.exec_container('6ba731551323', command[1])
    # ciscn_09
    # d._info()_info
    # d.runContainer()
    # print(d.getContainerStatus('17b2884cbd10'))
    # d.runContainers('django:1.9.1-python3')
    # d.runContainersWithId('123', '123', 'python /usr/src/nuckaggle/manage.py runserver 0.0.0.0:8000')
    # d.buildImageWithLog()
