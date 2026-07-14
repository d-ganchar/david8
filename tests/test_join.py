from dataclasses import dataclass

from parameterized import parameterized

from david8.expressions import Source, field_
from david8.expressions import col as c
from david8.expressions import desc as d
from david8.expressions import val as v
from david8.functions import concat
from david8.joins import asof, asof_left, inner, lateral, left, right
from david8.predicates import between, eq, eq_c, ge_c, gt, gt_c, le_c, lt_c
from david8.protocols.sql import AliasedProtocol, JoinProtocol, QueryProtocol
from tests.base_test import BaseTest


@dataclass(slots=True)
class _UsersTable(Source):
    _david8_source = 'users'

    id: AliasedProtocol = field_('id')
    name: AliasedProtocol = field_('name')
    country: AliasedProtocol = field_('country')


@dataclass(slots=True)
class _OrdersTable(Source):
    _david8_source = 'orders'

    id: AliasedProtocol = field_('id')
    user_id: AliasedProtocol = field_('user_id')
    product_id: AliasedProtocol = field_('product_id')
    billing_address: AliasedProtocol = field_('billing_address')
    shipping_address: AliasedProtocol = field_('shipping_address')


@dataclass(slots=True)
class _ProductsTable(Source):
    _david8_source = 'products'

    id: AliasedProtocol = field_('id')
    title: AliasedProtocol = field_('title')


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

    @parameterized.expand([
        (
            BaseTest
            .qb
            .select('*')
            .from_table('table_1')
            .join(asof().table('table_2').using('user_id', 'ts')),
            'SELECT * FROM table_1 ASOF JOIN table_2 USING (user_id, ts)'
        ),
        (
            BaseTest
            .qb
            .select('*')
            .from_table('table_1')
            .join(asof().table('table_2').on(
                eq_c('table_1.user_id', 'table_2.user_id'),
                gt_c('table_1.ts', 'table_2.ts'),
            )),
            'SELECT * FROM table_1 ASOF JOIN table_2 ON (table_1.user_id = table_2.user_id AND '
            'table_1.ts > table_2.ts)'
        ),
        # left
        (
            BaseTest
            .qb
            .select('*')
            .from_table('table_1')
            .join(asof_left().table('table_2').using('user_id', 'ts')),
            'SELECT * FROM table_1 ASOF LEFT JOIN table_2 USING (user_id, ts)'
        ),
        (
            BaseTest
            .qb
            .select('*')
            .from_table('table_1')
            .join(asof_left().table('table_2').on(
                eq_c('table_1.user_id', 'table_2.user_id'),
                gt_c('table_1.ts', 'table_2.ts'),
            )),
            'SELECT * FROM table_1 ASOF LEFT JOIN table_2 ON (table_1.user_id = table_2.user_id AND '
            'table_1.ts > table_2.ts)'
        ),
    ])
    def test_asof(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    def test_all_joins(self):
        query = (
            self.qb.select('*').from_table('orders', alias='o')
            .join(
                inner().table('customers').as_('c').on(eq_c('o.user_id', 'c.user_id')),
                left().table('shipping').as_('s').on(eq_c('o.order_id', 's.order_id')),
                right().table('discounts').as_('d').on(
                    eq_c('o.product_id', 'd.product_id'),
                    between('o.order_ts', c('d.valid_from'), c('d.valid_to'))
                ),
                asof().table('prices').as_('pr').on(
                    eq_c('o.product_id', 'pr.product_id'),
                    ge_c('o.order_ts', 'pr.price_ts')
                ),
                asof_left().table('order_status_history').as_('hist').on(
                    eq_c('o.order_id', 'hist.order_id'),
                    ge_c('o.order_ts', 'hist.status_ts')
                ),
                lateral().expression(
                    BaseTest.qb.select('note', 'distance')
                    .from_table('manager_notes', alias='mn')
                    .where(
                        eq_c('mn.user_id', 'c.user_id'),
                        le_c('mn.note_ts', 'o.order_ts')
                    )
                    .order_by(d('mn.note_ts'))
                    .limit(1)
                ).on(eq(v(1), v(1)))
            )
            .where(gt('o.order_ts', 1767225661))
            .order_by('o.order_id')
        )

        sql = query.get_sql()
        self.assertEqual(
            sql,
            'SELECT * FROM orders AS o INNER JOIN customers AS c ON (o.user_id = c.user_id) LEFT JOIN '
            'shipping AS s ON (o.order_id = s.order_id) RIGHT JOIN discounts AS d ON (o.product_id = d.product_id '
            'AND o.order_ts BETWEEN d.valid_from AND d.valid_to) ASOF JOIN prices AS pr ON '
            '(o.product_id = pr.product_id AND o.order_ts >= pr.price_ts) ASOF LEFT JOIN order_status_history AS hist '
            'ON (o.order_id = hist.order_id AND o.order_ts >= hist.status_ts) INNER JOIN LATERAL (SELECT note, '
            'distance FROM manager_notes AS mn WHERE mn.user_id = c.user_id AND mn.note_ts <= o.order_ts ORDER BY '
            'mn.note_ts DESC LIMIT 1) AS  ON (1 = 1) WHERE o.order_ts > %(p1)s ORDER BY o.order_id',
        )

        self.assertEqual(query.get_parameters(), {'p1': 1767225661})

    def test_join_db_name(self):
        # https://github.com/d-ganchar/david8/issues/60
        self.assertEqual(
            BaseTest.qb
            .select('*')
            .from_table('table1', alias='t1')
            .join(inner().table('table2', 'db2').as_('t2').using('p_id'))
            .get_sql(),
            'SELECT * FROM table1 AS t1 INNER JOIN db2.table2 AS t2 USING (p_id)'
        )

    def test_source(self):
        u = _UsersTable().as_('u')
        o = _OrdersTable().as_('o')
        p = _ProductsTable().as_('p')

        query = (
            self
            .qb
            .select(
                u.name.as_('username'),
                o.id.as_('order_id'),
                p.title.as_('product_name'),
                concat(o.billing_address, v('|'), o.shipping_address).as_('addresses'),
            )
            .from_source(u)
            .join(
                inner().source(o).on(eq(o.user_id, u.id)),
                inner().source(p).on(eq(p.id, o.product_id)),
            )
            .where(eq(u.country, 'PL'))
        )

        self.assertEqual(
            query.get_sql(),
            "SELECT u.name AS username, o.id AS order_id, p.title AS product_name, "
            "concat(o.billing_address, '|', o.shipping_address) AS addresses "
            "FROM users AS u "
            "INNER JOIN orders AS o ON (o.user_id = u.id) "
            "INNER JOIN products AS p ON (p.id = o.product_id) "
            "WHERE u.country = %(p1)s"
        )

        self.assertEqual(query.get_parameters(), {'p1': 'PL'})
