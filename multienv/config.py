import os


class Config:
    projects_config_file_path = None
    env_var_container_build = None
    dot_env_file_path = None
    laradock_root_folder = None

    def __init__(self,
                 projects: str = '../Projects.yml',
                 env_var_container_build: str = 'env_var_container_build.yml',
                 dot_env: str = '../../.env',
                 laradock_root_folder: str = '..'):
        self.projects_config_file_path = projects
        self.env_var_container_build = env_var_container_build
        self.dot_env_file_path = dot_env
        self.laradock_root_folder = laradock_root_folder

    def env_var_container_build_config(self):
        return os.path.abspath(self.env_var_container_build)

    def projects_config(self):
        return os.path.abspath(self.projects_config_file_path)

    def dot_env_file(self):
        return os.path.abspath(self.dot_env_file_path)

    def get_laradock_root_folder(self):
        return os.path.abspath(self.laradock_root_folder)

    def get_env_var_value(self, var_name: str) -> str:
        """
        Get env var value from var name.

        :param var_name:
        :return:
        """
        with open(self.dot_env_file()) as origin_file:
            for line in origin_file:
                name, var = line.partition("=")[::2]
                if name == var_name:
                    return var
