import yaml
import subprocess

from multienv.docker_compose import DockerCompose
from multienv.env_var import EnvVar
from multienv.exceptions import ProjectNotDefinedException, \
    ServicesNotDefinedException, InvalidYamlFileException, \
    ConfigFileNotFoundException
from multienv.project import Project
from multienv.service import Service
from multienv.config import Config


class MultiEnv:
    project_name = None
    project = None
    changed_env_vars = []
    docker_compose = None
    config = None

    def __init__(self, project_name, config, docker_compose=None):
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
        try:
            with open(self.config.projects_config(), 'r') as stream:
                project_definition = self.get_project_definition(stream)
                env_vars = self.get_defined_env_vars(project_definition)
                services = self.get_defined_services(project_definition)

                self.project = Project(
                    self.project_name,
                    env_vars,
                    services)
        except IOError:
            raise ConfigFileNotFoundException(
                error='Config file not found!',
                hint='Copy the file Projects.yml.example to Projects.yml and '
                     'setup your projects definitions. ')

    def get_defined_env_vars(self, project_definition):
        env_vars = []
        defined_env_vars = project_definition.get('env')
        if defined_env_vars:
            for var in defined_env_vars:
                for key in var:
                    value = str(var[key])

                env_vars.append(EnvVar(key, value, self.config))

        return env_vars

    def get_defined_services(self, project_definition):
        defined_services = project_definition.get('services')
        if not defined_services:
            raise ServicesNotDefinedException(
                error='No one service defined to project "' +
                      self.project_name,
                hint="""Setup the project services in your
        Projects.yml. E.g.:

        # Project name
        laravel_project:
          # Environment vars that will override the `.env` vars from laradock
          env:
            - PHP_VERSION: 7.3
          # The containers that will be executed
          services:
            - nginx
            - mysql
            - mailhog
          """)

        services = []
        for defined_service in defined_services:
            services.append(Service(defined_service))

        return services

    def define_env(self):
        for env_var in self.project.env_vars:
            # Get the var old value in .env file
            old_value = subprocess.check_output(
                ["grep " + env_var.name + " "
                 + self.config.dot_env_file()
                 + " | awk -F= '{print $2}'"],
                shell=True
            ).decode('utf-8')

            # Check if the key exists with the same value
            if old_value.strip() != env_var.value:
                self.changed_env_vars.append(env_var)

            # Create a backup of .env file and change the var value.
            subprocess.call(
                ["sed -i .bak '/^"
                 + env_var.name + "/s/=.*$/="
                 + env_var.value + "/' " + self.config.dot_env_file()],
                shell=True)

    def up(self):
        self.define_env()

        for env_var in self.changed_env_vars:
            for container in env_var.get_containers_to_rebuild():
                self.docker_compose.build(container)

        self.docker_compose.down()

        self.docker_compose.up(self.project.get_services_names(), detached=True)

        return True

    def get_project_definition(self, stream):
        try:
            projects_definitions = yaml.safe_load(stream)

            project_definition = projects_definitions.get(self.project_name)
            if not project_definition:
                raise ProjectNotDefinedException(
                    error='Project "' + self.project_name +
                          '" is not defined!',
                    hint='You must define the project on Project.yml '
                         'file or choose one of these projects: ' +
                         ', '.join(projects_definitions) + '.')

            return project_definition
        except yaml.YAMLError:
            raise InvalidYamlFileException(
                error='Error parsing project definitions file')
