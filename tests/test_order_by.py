from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.expressions import desc
from david8.protocols.sql import SelectProtocol
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

    @parameterized.expand([
        (
            BaseTest.qb.select('*').order_by(desc('height'), 'style', 'name'),
            'SELECT * FROM trees ORDER BY height DESC, style, name',
        ),
        (
            BaseTest.qb_w.select('*').order_by(desc('height'), 'style', 'name'),
            'SELECT "*" FROM "trees" ORDER BY "height" DESC, "style", "name"',
        ),
        (
            BaseTest.qb.select('*').order_by(desc(1), 2, 3),
            'SELECT * FROM trees ORDER BY 1 DESC, 2, 3',
        ),
        (
            BaseTest.qb_w.select('*').order_by(desc(1), 2, 3),
            'SELECT "*" FROM "trees" ORDER BY 1 DESC, 2, 3',
        ),
        (
            BaseTest.qb.select('*').order_by(
                'style',
                desc('height', 'age'),
                'name',
                desc('color', 'weight')
            ),
            'SELECT * FROM trees ORDER BY style, height DESC, age DESC, name, color DESC, weight DESC',
        ),
    ])
    def test_order_by_desc(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.from_table('trees').get_sql(), exp_sql)
