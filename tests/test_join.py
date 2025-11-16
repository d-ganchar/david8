from david8 import get_qb
from david8.dialects import PostgresDialect
from david8.predicates import eq_col
from tests.base_test import BaseTest

_qb_q = get_qb(PostgresDialect())      # quote mode
_qb_wq = get_qb(PostgresDialect(True)) # without quotes

class TestJoin(BaseTest):
    # TODO: thing and change JOIN interface
    def test_simple_left_join(self):
        query = (
            _qb_q
            .select('*')
            .from_table('users', 'u')
            .left_join(
                'orders',
                [
                    eq_col('o.user_id', 'u.id')
                ],
                'o'
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM users AS u LEFT JOIN orders AS o ON (o.user_id = u.id)'
        )

        query = (
            _qb_wq
            .select('*')
            .from_table('users', 'u')
            .left_join(
                'orders',
                [
                    eq_col('o.user_id', 'u.id')
                ],
                'o'
            )
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT "*" FROM "users" AS "u" LEFT JOIN "orders" AS o ON ("o.user_id" = "u.id")'
        )

    def test_simple_right_join(self):
        query = (
            _qb_q
            .select('*')
            .from_table('users', 'u')
            .right_join(
                'orders',
                [
                    eq_col('o.user_id', 'u.id')
                ],
                'o'
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM users AS u RIGHT JOIN orders AS o ON (o.user_id = u.id)'
        )

        query = (
            _qb_wq
            .select('*')
            .from_table('users', 'u')
            .right_join(
                'orders',
                [
                    eq_col('o.user_id', 'u.id')
                ],
                'o'
            )
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT "*" FROM "users" AS "u" RIGHT JOIN "orders" AS o ON ("o.user_id" = "u.id")'
        )

    def test_simple_inner_join(self):
        query = (
            _qb_q
            .select('*')
            .from_table('users', 'u')
            .inner_join(
                'orders',
                [
                    eq_col('o.user_id', 'u.id')
                ],
                'o'
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM users AS u INNER JOIN orders AS o ON (o.user_id = u.id)'
        )

        query = (
            _qb_wq
            .select('*')
            .from_table('users', 'u')
            .inner_join(
                'orders',
                [
                    eq_col('o.user_id', 'u.id')
                ],
                'o'
            )
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT "*" FROM "users" AS "u" INNER JOIN "orders" AS o ON ("o.user_id" = "u.id")'
        )
