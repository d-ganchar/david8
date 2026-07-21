from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.expressions import val as v
from david8.functions import add, mul
from david8.predicates import eq, lt
from tests.base_test import BaseTest


class TestWith(BaseTest):
    def test_with_recursive(self):
        qb = self.qb
        query = (
            qb
            .with_(
                (
                    'numbers',
                    qb
                    .select(v(1).as_('n'))
                    .union(
                        qb.select(add('n', v(1)))
                        .from_table('numbers')
                        .where(lt('n', 10))
                    ),
                ),
                (
                    'squares',
                    qb
                    .select('n', mul('n', 'n').as_('square'))
                    .from_table('numbers')
                ),
                (
                    'even_squares',
                    qb
                    .select('*')
                    .from_table('squares')
                ),
                recursive=True,
            )
            .select('*')
            .from_table('even_squares')
        )

        self.assertEqual(
            query.get_sql(),
            "WITH RECURSIVE numbers AS (SELECT 1 AS n UNION ALL SELECT (n + 1) FROM numbers WHERE n < %(p1)s), "
            "squares AS (SELECT n, (n * n) AS square FROM numbers), "
            "even_squares AS (SELECT * FROM squares) "
            "SELECT * FROM even_squares"
        )

        self.assertEqual(query.get_parameters(), {'p1': 10})

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
