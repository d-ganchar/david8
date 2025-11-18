from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.predicates import eq
from tests.base_test import BaseTest


class TestWith(BaseTest):

    @parameterized.expand([
        (
            BaseTest.qb,
            'WITH alias1 AS (SELECT * FROM legacy_table WHERE bad_category = %(p1)s), alias2 AS '
            '(SELECT * FROM new_table WHERE category = %(p2)s) SELECT * FROM legacy_table',
        ),
        (
            BaseTest.qb_w,
            'WITH "alias1" AS (SELECT "*" FROM "legacy_table" WHERE "bad_category" = %(p1)s), "alias2" AS '
            '(SELECT "*" FROM "new_table" WHERE "category" = %(p2)s) SELECT "*" FROM "legacy_table"',
        )
    ])
    def test_with_as_chain(self, qb: QueryBuilderProtocol, exp_sql: str) -> None:
        query = (
            qb.with_(
                ('alias1', qb.select('*').from_table('legacy_table').where(eq('bad_category', 'val1'))),
                ('alias2', qb.select('*').from_table('new_table').where(eq('category', 'val2'))),
            )
            .select('*')
            .from_table('legacy_table')
        )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'val1', 'p2': 'val2'}, query.get_parameters())

    @parameterized.expand([
        (
            BaseTest.qb,
            'WITH alias1 AS (SELECT * FROM legacy_table WHERE bad_category = %(p1)s), alias2 AS '
            '(SELECT * FROM new_table WHERE category = %(p2)s) SELECT * FROM legacy_table',
            'SELECT * FROM legacy_table WHERE bad_category = %(p1)s',
            'SELECT * FROM new_table WHERE category = %(p1)s',
        ),
        (
            BaseTest.qb_w,
            'WITH "alias1" AS (SELECT "*" FROM "legacy_table" WHERE "bad_category" = %(p1)s), "alias2" AS '
            '(SELECT "*" FROM "new_table" WHERE "category" = %(p2)s) SELECT "*" FROM "legacy_table"',
            'SELECT "*" FROM "legacy_table" WHERE "bad_category" = %(p1)s',
            'SELECT "*" FROM "new_table" WHERE "category" = %(p1)s',
        )
    ])
    def test_with_query_args(self, qb: QueryBuilderProtocol, exp_sql: str, q1_sql: str, q2_sql) -> None:
        query1 = qb.select('*').from_table('legacy_table').where(eq('bad_category', 'val1'))
        query2 = qb.select('*').from_table('new_table').where(eq('category', 'val2'))
        query = (
            qb.with_(
                ('alias1', query1),
                ('alias2', query2),
            )
            .select('*')
            .from_table('legacy_table')
        )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'val1', 'p2': 'val2'}, query.get_parameters())
        # check render and parameters after query.get_sql() for subqueries
        self.assertEqual(query1.get_sql(), q1_sql)
        self.assertEqual(query1.get_parameters(), {'p1': 'val1'})

        self.assertEqual(query2.get_sql(), q2_sql)
        self.assertEqual(query2.get_parameters(), {'p1': 'val2'})
