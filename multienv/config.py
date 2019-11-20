import os


class Config:
    projects_config_file_path = None
    env_var_container_build = None
    dot_env_file_path = None

    def __init__(self,
                 projects='../Projects.yml',
                 env_var_container_build='env_var_container_build.yml',
                 dot_env='../../.env'):
        self.projects_config_file_path = projects
        self.env_var_container_build = env_var_container_build
        self.dot_env_file_path = dot_env

    def env_var_container_build_config(self):
        return os.path.abspath(self.env_var_container_build)

    def projects_config(self):
        return os.path.abspath(self.projects_config_file_path)

    def dot_env_file(self):
        return os.path.abspath(self.dot_env_file_path)
