import uuid
import string
import random


def generate_flag_command(command: str):
    flag = f"flag{{{uuid.uuid4()}}}"
    return flag, command.format(flag=flag)


def generate_ssh_paasword(command: str):
    password = ''.join(random.sample(string.ascii_letters + string.digits, 12))
    return password, command.format(password=password)


if __name__ == '__main__':
    print(generate_flag_command('echo "{flag} > /flag"'))
    print(generate_ssh_paasword())
