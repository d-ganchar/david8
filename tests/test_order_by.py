from parameterized import parameterized

from david8 import QueryBuilderProtocol, get_qb
from david8.dialects import ClickhouseDialect
from tests.base_test import BaseTest


class TestOrderBy(BaseTest):

    @parameterized.expand([
        (
            get_qb(ClickhouseDialect()),
            'SELECT name, height FROM trees ORDER BY 1, 2',
        ),
        (
            get_qb(ClickhouseDialect(True)),
            'SELECT "name", "height" FROM "trees" ORDER BY 1, 2',
        )
    ])
    def test_order_by_int(self, qb, exp_sql):
        query = qb.select('name', 'height').from_table('trees').order_by(1)
        query.order_by(2)
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            get_qb(ClickhouseDialect()),
            'SELECT name, height, style FROM trees ORDER BY height DESC, style, name',
        ),
        (
            get_qb(ClickhouseDialect(True)),
            'SELECT "name", "height", "style" FROM "trees" ORDER BY "height" DESC, "style", "name"',
        )
    ])
    def test_order_by_str(self, qb: QueryBuilderProtocol, exp_sql: str):
        query = qb.select('name', 'height', 'style').from_table('trees').order_by_desc('height').order_by('style')
        query.order_by('name')

        self.assertEqual(query.get_sql(), exp_sql)
