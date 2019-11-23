import yaml

from multienv.docker_compose import DockerCompose
from multienv.env_var import EnvVar
from multienv.exceptions import ProjectNotDefinedException, \
    ServicesNotDefinedException, InvalidYamlFileException, \
    ConfigFileNotFoundException, InvalidProjectDefinitions
from multienv.helpers import sed_inplace
from multienv.project import Project
from multienv.service import Service
from multienv.config import Config
from multienv.webservers.web_server_factory import WebServerFactory
from multienv.webservers.webserver import WebServer


class MultiEnv:
    project_name = None
    project = None
    changed_env_vars = []
    docker_compose = None
    config = None

    def __init__(self, project_name, config, docker_compose=None,):
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

                self.project = Project(self.project_name,
                                       env_vars,
                                       services)

                server_service = self.get_defined_server_service(services)
                if server_service:
                    web_server = self.get_defined_server(project_definition,
                                                         server_service)
                    self.project.set_web_server(web_server)

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

    def get_defined_server(self, project_definition, server_service):
        defined_server = project_definition.get('server')
        if not defined_server:
            return

        return WebServerFactory(server_service)\
            .create(defined_server, self.config.get_laradock_root_folder())

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
            old_value = self.get_env_var_value(env_var.name)

            # Check if the key exists with the same value
            if old_value.strip() != env_var.value:
                self.changed_env_vars.append(env_var)

            # Change the var value.
            sed_inplace(self.config.dot_env_file(),
                        r'^' + env_var.name + '=.*$',
                        env_var.name + '=' + env_var.value)

    def up(self):
        self.define_env()
        self.define_web_server()

        for env_var in self.changed_env_vars:
            for container in env_var.get_containers_to_rebuild():
                self.docker_compose.build(container).call()

        self.docker_compose.down().call()

        self.docker_compose\
            .up(self.project.get_services_names(), detached=True)\
            .call()

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

    def get_env_var_value(self, var_name):
        with open(self.config.dot_env_file()) as origin_file:
            for line in origin_file:
                name, var = line.partition("=")[::2]
                if name == var_name:
                    return var

    def execute(self):
        return self.docker_compose\
            .execute(['workspace', 'bash'], user='laradock')\
            .call()

    def get_defined_server_service(self, services):
        server_services = []
        for service in services:
            if service.name in WebServer.available_web_servers:
                server_services.append(service.name)

        if len(server_services) == 0:
            return None

        if len(server_services) > 1:
            raise InvalidProjectDefinitions(
                error='More than one "server" service is defined',
                hint='You must choose between one of these: [' +
                     ', '.join(WebServer.available_web_servers) + ']'
            )

        return server_services[0]

    def define_web_server(self):
        if not self.project.web_server:
            return

        self.project.web_server.create_domain()
