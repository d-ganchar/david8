from parameterized import parameterized

from david8.expressions import col, param, val
from david8.protocols.sql import QueryProtocol
from tests.base_test import BaseTest


class TestExpressions(BaseTest):

    @parameterized.expand([
        # qb
        (
            BaseTest.qb.select(col('name')).from_table('users'),
            'SELECT name FROM users'
        ),
        (
            BaseTest.qb.select(col('legacy').as_('fixed')).from_table('users'),
            'SELECT legacy AS fixed FROM users'
        ),
        # qb_w
        (
            BaseTest.qb_w.select(col('name')).from_table('users'),
            'SELECT "name" FROM "users"'
        ),
        (
            BaseTest.qb_w.select(col('legacy').as_('fixed')).from_table('users'),
            'SELECT "legacy" AS "fixed" FROM "users"'
        ),
    ])
    def test_col(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.select(param('name')).from_table('users'),
            'SELECT %(p1)s FROM users',
            {'p1': 'name'}
        ),
        (
            BaseTest.qb.select(param('name').as_('alias')).from_table('users'),
            'SELECT %(p1)s AS alias FROM users',
            {'p1': 'name'}
        )
    ])
    def test_param(self, query: QueryProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

    @parameterized.expand([
        (
            BaseTest.qb.select(val('name')).from_table('users'),
            "SELECT 'name' FROM users",
        ),
        (
            BaseTest.qb_w.select(val('name').as_('alias')).from_table('users'),
            'SELECT \'name\' AS "alias" FROM "users"',
        ),
        (
            BaseTest.qb.select(val(1)).from_table('users'),
            "SELECT 1 FROM users",
        ),
        (
            BaseTest.qb_w.select(val(1).as_('alias')).from_table('users'),
            'SELECT 1 AS "alias" FROM "users"',
        ),
        (
            BaseTest.qb.select(val(0.69)).from_table('users'),
            "SELECT 0.69 FROM users",
        ),
        (
            BaseTest.qb_w.select(val(0.96).as_('alias')).from_table('users'),
            'SELECT 0.96 AS "alias" FROM "users"',
        )
    ])
    def test_val(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
