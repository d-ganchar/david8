from parameterized import parameterized

from david8.predicates import eq
from david8.protocols.sql import UpdateProtocol
from tests.base_test import BaseTest


class TestInsert(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .insert()
            .into('movie')
            .value('name', 'Aliens')
            .value('year', 1986),
            'INSERT INTO movie (name, year) VALUES (%(p1)s, %(p2)s)',
            {'p1': 'Aliens', 'p2': 1986},
        ),
        (
            BaseTest.qb
            .insert()
            .into('movie', 'art')
            .columns('name', 'year')
            .from_select(BaseTest.qb.select('name', 'year').from_table('old_movie').where(eq('name', 'Aliens'))),
            'INSERT INTO art.movie (name, year) SELECT name, year FROM old_movie WHERE name = %(p1)s',
            {'p1': 'Aliens'},
        ),
        (
            BaseTest.qb_w
            .insert()
            .into('movie')
            .value('name', 'Aliens')
            .value('year', 1986),
            'INSERT INTO "movie" ("name", "year") VALUES (%(p1)s, %(p2)s)',
            {'p1': 'Aliens', 'p2': 1986},
        ),
        (
            BaseTest.qb_w
            .insert()
            .into('movie', 'art')
            .columns('name', 'year')
            .from_select(BaseTest.qb.select('name', 'year').from_table('old_movie').where(eq('name', 'Aliens'))),
            'INSERT INTO "art"."movie" ("name", "year") SELECT "name", "year" FROM "old_movie" WHERE "name" = %(p1)s',
            {'p1': 'Aliens'},
        ),
    ])
    def test_insert(self, query: UpdateProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
