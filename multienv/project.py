class Project:
    name = None
    env_vars = []
    services = []

    def __init__(self, name, env_vars, services):
        self.name = name
        self.env_vars = env_vars
        self.services = services

    def get_services_names(self):
        services_names = []
        for service in self.services:
            services_names.append(service.name)

        return services_names
