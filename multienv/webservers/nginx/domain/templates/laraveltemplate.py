from multienv.helpers import sed_inplace


class LaravelTemplate:
    def replace_content(self, filename, site, root):
        sed_inplace(filename, 'laravel.test', site)
        sed_inplace(filename,
                    'root /var/www/laravel/public',
                    'root /var/www/' + root)
