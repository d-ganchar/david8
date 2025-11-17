from parameterized import parameterized

from david8.joins import inner, left, right
from david8.predicates import eq_col
from david8.protocols.sql import QueryProtocol
from tests.base_test import BaseTest


class TestJoin(BaseTest):
    @parameterized.expand([
        # left
        (
            BaseTest
            .qb
            .select('*')
            .from_table('users', 'u')
            .join(left().table('orders').on(eq_col('o.user_id', 'u.id')).as_('o')),
            'SELECT * FROM users AS u LEFT JOIN orders AS o ON (o.user_id = u.id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('users', 'u')
            .join(left().table('orders').on(eq_col('o.user_id', 'u.id')).as_('o')),
            'SELECT "*" FROM "users" AS "u" LEFT JOIN "orders" AS "o" ON ("o"."user_id" = "u"."id")'
        ),
        # right
        (
            BaseTest
            .qb
            .select('*')
            .from_table('users', 'u')
            .join(right().table('orders').on(eq_col('o.user_id', 'u.id')).as_('o')),
            'SELECT * FROM users AS u RIGHT JOIN orders AS o ON (o.user_id = u.id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('users', 'u')
            .join(right().table('orders').on(eq_col('o.user_id', 'u.id')).as_('o')),
            'SELECT "*" FROM "users" AS "u" RIGHT JOIN "orders" AS "o" ON ("o"."user_id" = "u"."id")'
        ),
        # inner
        (
            BaseTest
            .qb
            .select('*')
            .from_table('users', 'u')
            .join(inner().table('orders').on(eq_col('o.user_id', 'u.id')).as_('o')),
            'SELECT * FROM users AS u INNER JOIN orders AS o ON (o.user_id = u.id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('users', 'u')
            .join(inner().table('orders').on(eq_col('o.user_id', 'u.id')).as_('o')),
            'SELECT "*" FROM "users" AS "u" INNER JOIN "orders" AS "o" ON ("o"."user_id" = "u"."id")'
        ),
    ])
    def test_simple_join_on(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        # left
        (
            BaseTest
            .qb
            .select('*')
            .from_table('orders')
            .join(left().table('order_items').using('order_id', 'user_id')),
            'SELECT * FROM orders LEFT JOIN order_items USING (order_id, user_id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('orders')
            .join(left().table('order_items').using('order_id', 'user_id')),
            'SELECT "*" FROM "orders" LEFT JOIN "order_items" USING ("order_id", "user_id")'
        ),
        # right
        (
            BaseTest
            .qb
            .select('*')
            .from_table('orders')
            .join(left().table('order_items').using('order_id', 'user_id')),
            'SELECT * FROM orders LEFT JOIN order_items USING (order_id, user_id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('orders')
            .join(left().table('order_items').using('order_id', 'user_id')),
            'SELECT "*" FROM "orders" LEFT JOIN "order_items" USING ("order_id", "user_id")'
        ),
        # inner
        (
            BaseTest
            .qb
            .select('*')
            .from_table('orders')
            .join(left().table('order_items').using('order_id', 'user_id')),
            'SELECT * FROM orders LEFT JOIN order_items USING (order_id, user_id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('orders')
            .join(left().table('order_items').using('order_id', 'user_id')),
            'SELECT "*" FROM "orders" LEFT JOIN "order_items" USING ("order_id", "user_id")'
        ),
    ])
    def test_simple_join_using(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
