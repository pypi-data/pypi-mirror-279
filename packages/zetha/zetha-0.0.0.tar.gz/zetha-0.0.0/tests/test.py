import logging
import unittest as test

from zetha import Connect, folha as f, migrator as m


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

conn = Connect(
    'test',
    username='postgres',
    password='12345',
    host='localhost',
)


class Tests(test.TestCase):
    def connection(self):
        with conn.session as session:
            new_folha = f.Cargo(descricao='PREFEITO')
            session.add(new_folha)
            session.commit()


if __name__ == '__main__':
    test.main()
