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
            BaseTest.qb.drop().table('events', if_exists=True),
            'DROP TABLE IF EXISTS events',
        ),
        (
            BaseTest.qb.drop().table('events', 'game', if_exists=True),
            'DROP TABLE IF EXISTS game.events',
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

    @parameterized.expand([
        (
            BaseTest.qb.drop().view('events'),
            'DROP VIEW events',
        ),
        (
            BaseTest.qb.drop().view('events', 'game'),
            'DROP VIEW game.events',
        ),
        (
            BaseTest.qb.drop().view('events', if_exists=True),
            'DROP VIEW IF EXISTS events',
        ),
        (
            BaseTest.qb.drop().view('events', 'game', if_exists=True),
            'DROP VIEW IF EXISTS game.events',
        ),
        (
            BaseTest.qb_w.drop().view('events'),
            'DROP VIEW "events"'
        ),
        (
            BaseTest.qb_w.drop().view('events', 'game'),
            'DROP VIEW "game"."events"'
        ),
    ])
    def test_drop_view(self, view: QueryProtocol, exp_sql: str):
        self.assertEqual(view.get_sql(), exp_sql)
