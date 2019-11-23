import abc


class Template:
    def __init__(self, site, root):
        """
        Create an instance of the template.

        :param site: The site to configure
        :param root: The root folder to configure
        """
        self.root = root
        self.site = site

    @abc.abstractmethod
    def replace_content(self, filename):
        """
        Replace the template file content with site and root.

        :param filename: The file to be replaced
        :return:
        :rtype: None
        """
        pass
