from typing import List, Optional

from multienv.database.database import Database
from multienv.env_var import EnvVar

from multienv.database.dbms.dbms import DBMS
from multienv.exceptions import InvalidProjectDefinitions
from multienv.service import Service
from multienv.web_servers.web_server import WebServer


class Project:
    __name: str
    services: List[Service]
    env_vars: List[EnvVar] = []
    web_server: WebServer = None
    dbms: DBMS = None
    __databases: List[Database] = []

    def __init__(self, name: str, services: List[Service]):
        self.__name = name
        self.services = services

    def get_services_names(self):
        services_names = []
        for service in self.services:
            services_names.append(service.name)

        return services_names

    def set_env_vars(self, env_vars: List[EnvVar]):
        self.env_vars = env_vars
        return self

    def set_web_server(self, web_server: WebServer):
        self.web_server = web_server
        return self

    def set_dbms(self, dbms: DBMS):
        """
        Set the Database Management System handler.

        :param dbms:
        :return:
        """
        self.dbms = dbms
        return self

    def set_databases(self, databases: List[Database]):
        self.__databases = databases
        return self

    def get_defined_web_server_service(self) -> Optional[str]:
        """
        Get the web server service defined on config file.

        :return: The web server service or None if no one web server service
                 was defined
        :raises InvalidProjectDefinitions if more than one web server service
                was defined.
        """
        web_server_services = []
        for service in self.services:
            if service.name in WebServer.available_web_servers:
                web_server_services.append(service.name)

        if len(web_server_services) == 0:
            return None

        if len(web_server_services) > 1:
            raise InvalidProjectDefinitions(
                error='More than one "server" service is defined',
                hint='You must choose between one of these: [' +
                     ', '.join(WebServer.available_web_servers) + ']'
            )

        return web_server_services[0]

    def get_defined_dbms_service(self) -> Optional[str]:
        """
        Get the defined Database Management System service name.

        :return: The DBMS service name or None
        """
        dbms_services = []
        for service in self.services:
            if service.name in DBMS.available_dbms:
                dbms_services.append(service.name)

        if len(dbms_services) == 0:
            return None

        if len(dbms_services) > 1:
            raise InvalidProjectDefinitions(
                error='More than one "Database Management System" service is '
                      'defined',
                hint='You must choose between one of these: [' +
                     ', '.join(DBMS.available_dbms) + ']'
            )

        return dbms_services[0]

    def get_databases(self) -> List[Database]:
        return self.__databases

    def get_name(self) -> str:
        return self.__name

