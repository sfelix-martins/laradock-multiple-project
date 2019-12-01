from typing import List, Optional, TextIO

import yaml

from multienv.config import Config
from multienv.database.database import Database
from multienv.database.dbms.dbms import DBMS
from multienv.database.dbms.dbms_factory import DBMSFactory
from multienv.env_var import EnvVar

from multienv.exceptions import ConfigFileNotFoundException, \
    ProjectNotDefinedException, InvalidYamlFileException, \
    ServicesNotDefinedException
from multienv.project.project import Project
from multienv.service import Service
from multienv.web_servers.web_server import WebServer
from multienv.web_servers.web_server_factory import WebServerFactory


class ProjectBuilder:
    project: Project = None
    name: str
    config: Config
    __definitions: dict = None

    def __init__(self, name, config):
        self.name = name
        self.config = config

        self.__build()

    def __build(self):
        """
        Build the projects definitions from config file and define the project.

        :raises ConfigFileNotFoundException if the config file not found.
        """
        try:
            with open(self.config.projects_config(), 'r') as stream:
                self.__set_project_definition_from_config(stream)

            self.__build_project()
        except IOError:
            raise ConfigFileNotFoundException(
                error='Config file not found!',
                hint='Copy the file Projects.yml.example to Projects.yml and '
                     'setup your projects definitions. ')

    def __set_project_definition_from_config(self, stream: TextIO):
        """
        Set project definitions from config file.

        :param stream: The yaml config file content.
        :raises ProjectNotDefinedException
        :raises InvalidYamlFileException
        """
        try:
            projects_definitions = yaml.safe_load(stream)

            project_definition = projects_definitions.get(self.name)
            if not project_definition:
                raise ProjectNotDefinedException(
                    error='Project "' + self.name +
                          '" is not defined!',
                    hint='You must define the project on Project.yml '
                         'file or choose one of these projects: ' +
                         ', '.join(projects_definitions) + '.')

            self.__definitions = project_definition
        except yaml.YAMLError:
            raise InvalidYamlFileException(
                error='Error parsing project definitions file')

    def __get_env_vars(self) -> List[EnvVar]:
        """
        Get the env vars from definitions
        """
        env_vars = []
        defined_env_vars = self.__definitions.get('env')
        if defined_env_vars:
            for var in defined_env_vars:
                for key in var:
                    value = str(var[key])

                    env_vars.append(EnvVar(key, value, self.config))

        return env_vars

    def __get_services(self) -> List[Service]:
        """
        Get the services defined on config file.

        :return: A list of Service
        :raises ServicesNotDefinedException if has no one service defined on
                config file.
        """
        defined_services = self.__definitions.get('services')
        if not defined_services:
            raise ServicesNotDefinedException(
                error='No one service defined to project "' +
                      self.name,
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
    - mailhog""")

        services = []
        for defined_service in defined_services:
            services.append(Service(defined_service))

        return services

    def __build_project(self):
        """
        Build the project instance based on definition got from config file.
        """
        project = Project(self.name, self.__get_services())

        env_vars = self.__get_env_vars()
        if env_vars:
            project.set_env_vars(env_vars)

        web_server_service = project.get_defined_web_server_service()
        if web_server_service:
            web_server = self.__get_web_server_instance(web_server_service)
            project.set_web_server(web_server)

        dbms_service = project.get_defined_dbms_service()
        if dbms_service:
            dbms = self.__get_dbms_instance(dbms_service)
            if dbms:
                project.set_dbms(dbms)

                databases = self.__get_defined_databases(dbms)
                if databases:
                    project.set_databases(databases)

        self.project = project

    def __get_web_server_instance(self, name) -> Optional[WebServer]:
        """
        Get Web Server handler instance by name.

        :param name: The name of the web server service
        :return: The Web Server handler instance.
        """
        defined_server = self.__definitions.get('server')
        if not defined_server:
            # TODO: Print WARNING when has no one Web Server service defined and
            #       has server configs.
            return None

        return WebServerFactory(name) \
            .create(defined_server, self.config.get_laradock_root_folder())

    def __get_dbms_instance(self, name) -> Optional[DBMS]:
        """
        Get Database Management System handler instance by name.

        :param name: The name of the DBMS service
        :return: The DBMS handler instance.
        """
        databases = self.__definitions.get('databases')

        if not databases:
            # TODO: Print WARNING when has no one DBMS service defined and
            #       has databases configs.
            return None

        return DBMSFactory(name).create(self.config.get_laradock_root_folder())

    def __get_defined_databases(self, dbms: DBMS) -> List[Database]:
        """
        Get the defined databases from configs.

        :return: Return a list of Database.
        """

        # Get databases user
        user = self.config.get_env_var_value(dbms.user_attribute)

        databases = []
        defined_databases = self.__definitions.get('databases')
        if defined_databases:
            for db_name in defined_databases:
                databases.append(Database(db_name, user))

        return databases
