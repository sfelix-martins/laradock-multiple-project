from multienv.helpers import sed_inplace


class Template:
    def __init__(self, site, root):
        """
       Create an instance of the template.

       :param site: The site to configure
       :param root: The root folder to configure
       """
        self.site = site
        self.root = root

    def replace_content(self, filename):
        """
        Replace the template file content with site and root.

        :param filename: The file to be replaced
        :return:
        :rtype: None
        """
        print('site', self.site)
        sed_inplace(filename, 'sample.test', self.site)
        sed_inplace(filename,
                    'DocumentRoot /var/www/sample/public/',
                    'DocumentRoot /var/www/' + self.root)
        sed_inplace(filename,
                    '<Directory "/var/www/sample/public/">',
                    '<Directory "/var/www/' + self.root + '">')
