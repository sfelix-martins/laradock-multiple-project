from multienv.helpers import sed_inplace


class CaddyTemplate:
    def __init__(self, site, root, https=False):
        """
       Create an instance of the template.

       :param site: The site to configure
       :param root: The root folder to configure
       :param https: Check if should use https
       """
        self.site = site
        self.root = root
        self.https = https

    def replace_content(self, filename):
        """
        Replace the template file content with site and root.

        :param filename: The file to be replaced
        :return:
        :rtype: None
        """
        site = self.site
        if self.https:
            sed_inplace(filename,
                        '#tls self_signed',
                        'tls self_signed')
            site = 'https://' + site

        sed_inplace(filename, '0.0.0.0', site)
        sed_inplace(filename,
                    'root /var/www/public',
                    'root /var/www/' + self.root)


