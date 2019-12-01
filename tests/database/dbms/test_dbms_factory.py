import unittest

from multienv.database.dbms.dbms_factory import DBMSFactory
from multienv.exceptions import InvalidArgumentException


class DBMSFactoryTestCase(unittest.TestCase):
    def test_create_dbms_factory_with_not_available_dbms(self):
        with self.assertRaises(InvalidArgumentException):
            DBMSFactory('not_available')

    def test_create_dbms_with_not_implemented_dbms(self):
        with self.assertRaises(NotImplementedError):
            DBMSFactory('postgres').create('..')


if __name__ == '__main__':
    unittest.main()
