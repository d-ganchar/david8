from parameterized import parameterized

from david8.expressions import col, val
from david8.predicates import eq
from david8.protocols.sql import UpdateProtocol
from tests.base_test import BaseTest


class TestUpdate(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .update()
            .table('movie')
            .set_('name', 'aliens')
            .where(eq('movie', '')),
            'UPDATE movie SET name = %(p1)s WHERE movie = %(p2)s',
            {'p1': 'aliens', 'p2': ''},
        ),
        (
            BaseTest.qb_w
            .update()
            .table('movie')
            .set_('name', 'aliens')
            .where(eq('movie', '')),
            'UPDATE "movie" SET "name" = %(p1)s WHERE "movie" = %(p2)s',
            {'p1': 'aliens', 'p2': ''},
        ),
        (
            BaseTest.qb
            .update()
            .table('movie', 'm', 'art')
            .set_('name', BaseTest.qb.select(val('aliens')))
            .set_('directed_by', BaseTest.qb.select(val('James Cameron')))
            .where(eq('movie', '')),
            "UPDATE art.movie AS m SET name = (SELECT 'aliens'), directed_by = (SELECT 'James Cameron')"
            " WHERE movie = %(p1)s",
            {'p1': ''},
        ),
        (
            BaseTest.qb
            .update()
            .table('movie')
            .set_('name', col('new_name'))
            .where(eq('movie', '')),
            'UPDATE movie SET name = new_name WHERE movie = %(p1)s',
            {'p1': ''},
        ),
    ])
    def test_update(self, query: UpdateProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
