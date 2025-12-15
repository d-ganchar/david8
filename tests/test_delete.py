from parameterized import parameterized

from david8.predicates import eq, le
from david8.protocols.sql import UpdateProtocol
from tests.base_test import BaseTest


class TestDelete(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .delete()
            .from_table('movie')
            .where(eq('name', ''), le('year', 1888)),
            'DELETE FROM movie WHERE name = %(p1)s AND year <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb
            .delete()
            .from_table('movie', 'art')
            .where(eq('name', ''), le('year', 1888)),
            'DELETE FROM art.movie WHERE name = %(p1)s AND year <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb_w
            .delete()
            .from_table('movie')
            .where(eq('name', ''), le('year', 1888)),
            'DELETE FROM "movie" WHERE "name" = %(p1)s AND "year" <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb_w
            .delete()
            .from_table('movie', 'art')
            .where(eq('name', ''), le('year', 1888)),
            'DELETE FROM "art"."movie" WHERE "name" = %(p1)s AND "year" <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
    ])
    def test_delete(self, query: UpdateProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
