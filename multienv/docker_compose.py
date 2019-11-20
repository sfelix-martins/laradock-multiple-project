import subprocess


class DockerCompose:
    cwd = None
    base_cmd = 'docker-compose'

    def __init__(self, cwd='..'):
        self.cwd = cwd

    def build(self, container):
        self.call(self.base_cmd + ' build ' + container)

    def down(self):
        self.call(self.base_cmd + ' down')

    def up(self, containers, detached=False):
        cmd_list = [self.base_cmd, 'up']
        if detached:
            cmd_list.append('-d')

        cmd_list += containers

        cmd = ' '.join(cmd_list)

        self.call(cmd)

    def call(self, cmd):
        subprocess.call([cmd], shell=True, cwd=self.cwd)
