import yaml

from multienv.exceptions import InvalidYamlFileException, \
    EnvVarContainerBuildNotFoundException


class EnvVar:
    name = None
    value = None
    config = None

    def __init__(self, name, value, config):
        self.name = name
        self.value = value
        self.config = config

    def get_containers_to_rebuild(self):
        try:
            with open(self.config.env_var_container_build_config(),
                      'r') as stream:
                containers = self.get_containers_from_stream(stream)
                containers.sort()

                return containers

        except IOError:
            raise EnvVarContainerBuildNotFoundException(
                error='env_var_container_build.yml config file not found!')

    def get_containers_from_stream(self, stream):
        try:
            env_vars_containers_build = yaml.safe_load(stream)

            containers = env_vars_containers_build.get(self.name)

            return list(dict.fromkeys(containers)) if containers else []
        except yaml.YAMLError:
            raise InvalidYamlFileException(
                error='Error parsing env_var_container_build mapping '
                      'definitions file')
