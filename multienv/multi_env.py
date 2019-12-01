from typing import Optional, List

from multienv.env_var import EnvVar

from multienv.docker_compose import DockerCompose
from multienv.helpers import sed_inplace
from multienv.project.project import Project
from multienv.project.project_builder import ProjectBuilder
from multienv.config import Config


class MultiEnv:
    project_name: str
    project: Project
    changed_env_vars: List[EnvVar] = []
    docker_compose: DockerCompose
    config: Config

    def __init__(self,
                 project_name: str,
                 config: Config,
                 docker_compose: Optional[DockerCompose] = None):
        self.project_name = project_name
        if not isinstance(config, Config):
            raise TypeError('The param config must be an instance of Config '
                            'class')
        self.config = config

        if not docker_compose:
            docker_compose = DockerCompose()
        elif not isinstance(docker_compose, DockerCompose):
            raise TypeError('The param docker_compose must be an instance of '
                            'DockerCompose class')
        self.docker_compose = docker_compose

        self.define_project()

    def define_project(self):
        definitions = ProjectBuilder(self.project_name, self.config)

        self.project = definitions.project

    def define_env(self):
        self.change_env_vars(self.project.env_vars)

    def up(self):
        self.define_env()
        self.define_web_server()
        self.define_databases()

        for env_var in self.changed_env_vars:
            for container in env_var.get_containers_to_rebuild():
                self.docker_compose.build(container).call()

        self.docker_compose.down().call()

        self.docker_compose\
            .up(self.project.get_services_names(), detached=True)\
            .call()

        return True

    def get_env_var_value(self, var_name: str):
        with open(self.config.dot_env_file()) as origin_file:
            for line in origin_file:
                name, var = line.partition("=")[::2]
                if name == var_name:
                    return var

    def execute(self):
        return self.docker_compose\
            .execute(['workspace', 'bash'], user='laradock')\
            .call()

    def define_web_server(self):
        if not self.project.web_server:
            return

        self.project.web_server.create_domain()

    def define_databases(self):
        if not self.project.get_databases():
            return

        self.project.dbms.create_databases(self.project)

        database_env_vars = [
            EnvVar(
                'DATA_PATH_HOST',
                f'~/.laradock/data/{self.project_name}',
                self.config
            ),
            EnvVar(
                'MYSQL_ENTRYPOINT_INITDB',
                f'./mysql/docker-entrypoint-initdb.d/{self.project_name}',
                self.config
            )
        ]

        self.change_env_vars(database_env_vars)

    def change_env_vars(self, env_vars: List[EnvVar], create: bool = True):
        """
        Change the env vars value.

        :param env_vars:
        :param create: Check if should create a var if not exists
        :return:
        """

        for env_var in env_vars:
            # Get the var old value in .env file
            old_value = self.get_env_var_value(env_var.name)
            if not old_value:
                if create:
                    with open(self.config.dot_env_file(), 'a') as file:
                        file.write(f'{env_var.name}={env_var.value}')
                return

            # Check if the key exists with the same value
            if old_value.strip() != env_var.value:
                self.changed_env_vars.append(env_var)

            # Change the var value.
            sed_inplace(self.config.dot_env_file(),
                        r'^' + env_var.name + '=.*$',
                        env_var.name + '=' + env_var.value)
