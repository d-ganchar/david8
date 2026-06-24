from parameterized import parameterized

from david8.joins import inner, lateral, left, right
from david8.predicates import eq_c, lt_c
from david8.protocols.sql import JoinProtocol, QueryProtocol
from tests.base_test import BaseTest


class TestJoin(BaseTest):
    @parameterized.expand([
        # left
        (
            BaseTest
            .qb
            .select('*')
            .from_table('users', 'u')
            .join(left().table('orders').on(eq_c('o.user_id', 'u.id')).as_('o')),
            'SELECT * FROM users AS u LEFT JOIN orders AS o ON (o.user_id = u.id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('users', 'u')
            .join(left().table('orders').on(eq_c('o.user_id', 'u.id')).as_('o')),
            'SELECT "*" FROM "users" AS "u" LEFT JOIN "orders" AS "o" ON ("o"."user_id" = "u"."id")'
        ),
        # right
        (
            BaseTest
            .qb
            .select('*')
            .from_table('users', 'u')
            .join(right().table('orders').on(eq_c('o.user_id', 'u.id')).as_('o')),
            'SELECT * FROM users AS u RIGHT JOIN orders AS o ON (o.user_id = u.id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('users', 'u')
            .join(right().table('orders').on(eq_c('o.user_id', 'u.id')).as_('o')),
            'SELECT "*" FROM "users" AS "u" RIGHT JOIN "orders" AS "o" ON ("o"."user_id" = "u"."id")'
        ),
        # inner
        (
            BaseTest
            .qb
            .select('*')
            .from_table('users', 'u')
            .join(inner().table('orders').on(eq_c('o.user_id', 'u.id')).as_('o')),
            'SELECT * FROM users AS u INNER JOIN orders AS o ON (o.user_id = u.id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('users', 'u')
            .join(inner().table('orders').on(eq_c('o.user_id', 'u.id')).as_('o')),
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

    @parameterized.expand([
        # using
        (
            BaseTest
            .qb
            .select('*')
            .from_table('orders')
            .join(
                left()
                .query(BaseTest.qb.select('*').from_table('users'))
                .using('order_id', 'user_id')
            ),
            'SELECT * FROM orders LEFT JOIN (SELECT * FROM users) USING (order_id, user_id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('orders')
            .join(
                left()
                .query(BaseTest.qb.select('*').from_table('users'))
                .using('order_id', 'user_id')
            ),
            'SELECT "*" FROM "orders" LEFT JOIN (SELECT "*" FROM "users") USING ("order_id", "user_id")'
        ),
        # on
        (
            BaseTest
            .qb
            .select('*')
            .from_table('users', 'u')
            .join(
                left()
                .query(BaseTest.qb.select('*').from_table('users'))
                .on(eq_c('o.user_id', 'u.id'))
                .as_('o')
            ),
            'SELECT * FROM users AS u LEFT JOIN (SELECT * FROM users) AS o ON (o.user_id = u.id)'
        ),
        (
            BaseTest
            .qb_w
            .select('*')
            .from_table('users', 'u')
            .join(
                left()
                .query(BaseTest.qb.select('*').from_table('users'))
                .on(eq_c('o.user_id', 'u.id'))
                .as_('o')
            ),
            'SELECT "*" FROM "users" AS "u" LEFT JOIN (SELECT "*" FROM "users") AS "o" ON ("o"."user_id" = "u"."id")'
        ),
    ])
    def test_join_from_query(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            (
                lateral()
                .expression(
                    BaseTest.qb
                    .select('store_id', 'distance')
                    .from_table('stores', alias='s')
                )
                .as_('nearby')
                .on(lt_c('nearby.distance', 'c.max_km'))
            ),
            'SELECT * FROM customers AS c '
            'INNER JOIN LATERAL (SELECT store_id, distance FROM stores AS s) AS nearby ON (nearby.distance < c.max_km)'
        ),
    ])
    def test_literal_join(self, join: JoinProtocol, exp_sql: str):
        query = self.qb.select('*').from_table('customers', alias='c').join(join)
        self.assertEqual(query.get_sql(), exp_sql)
