import uuid


def generate_flag_command(command:str):
    flag = f"flag{{{uuid.uuid4()}}}"
    return flag,command.format(flag=flag)


if __name__ == '__main__':
    print(generate_flag_command('echo "{flag} > /flag"'))