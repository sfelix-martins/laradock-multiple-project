import subprocess


def mount(params):
    return ' '.join(params)


class DockerCompose:
    cwd = None
    base_cmd = 'docker-compose'
    cmd = None

    def __init__(self, cwd='..'):
        self.cwd = cwd

    def build(self, container):
        return self.mount(['build', container])

    def down(self):
        return self.mount(['down'])

    def up(self, containers, detached=True):
        cmd_list = ['up']
        if detached:
            cmd_list.append('-d')

        cmd_list += containers

        return self.mount(cmd_list)

    def exec(self, containers, user=None):
        cmd_list = ['exec']
        if user:
            cmd_list.append('--user=' + user)

        cmd_list += containers

        return self.mount(cmd_list)

    def call(self):
        if not self.cmd:
            raise RuntimeError('Command not defined')

        return subprocess.call([self.cmd], shell=True, cwd=self.cwd)

    def mount(self, params):
        self.cmd = mount([self.base_cmd] + params)

        return self
