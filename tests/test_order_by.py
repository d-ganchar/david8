from parameterized import parameterized

from david8 import QueryBuilderProtocol
from tests.base_test import BaseTest


class TestOrderBy(BaseTest):

    @parameterized.expand([
        (
            BaseTest.qb,
            'SELECT name, height FROM trees ORDER BY 1, 2',
        ),
        (
            BaseTest.qb_w,
            'SELECT "name", "height" FROM "trees" ORDER BY 1, 2',
        )
    ])
    def test_order_by_int(self, qb, exp_sql):
        query = qb.select('name', 'height').from_table('trees').order_by(1)
        query.order_by(2)
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb,
            'SELECT name, height, style FROM trees ORDER BY height DESC, style, name',
        ),
        (
            BaseTest.qb_w,
            'SELECT "name", "height", "style" FROM "trees" ORDER BY "height" DESC, "style", "name"',
        )
    ])
    def test_order_by_str(self, qb: QueryBuilderProtocol, exp_sql: str):
        query = qb.select('name', 'height', 'style').from_table('trees').order_by_desc('height').order_by('style')
        query.order_by('name')

        self.assertEqual(query.get_sql(), exp_sql)
