class Database:
    name: str
    user: str
    __default_user = 'default'

    def __init__(self, name: str, user: str = None):
        self.name = name.strip()

        if not user:
            user = self.__default_user
        self.user = user.strip()
