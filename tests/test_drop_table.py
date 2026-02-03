from parameterized import parameterized

from david8.protocols.sql import QueryProtocol
from tests.base_test import BaseTest


class TestDropTable(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb.drop().table('events'),
            'DROP TABLE events',
        ),
        (
            BaseTest.qb.drop().table('events', 'game'),
            'DROP TABLE game.events',
        ),
        (
            BaseTest.qb_w.drop().table('events'),
            'DROP TABLE "events"'
        ),
        (
            BaseTest.qb_w.drop().table('events', 'game'),
            'DROP TABLE "game"."events"'
        ),
    ])
    def test_drop_table(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
