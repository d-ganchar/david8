from parameterized import parameterized

from david8.expressions import Column, Parameter, Value
from david8.protocols.sql import QueryProtocol
from tests.base_test import BaseTest


class TestExpressions(BaseTest):

    @parameterized.expand([
        # qb
        (
            BaseTest.qb.select(Column('name')).from_table('users'),
            'SELECT name FROM users'
        ),
        (
            BaseTest.qb.select(Column('legacy').as_('fixed')).from_table('users'),
            'SELECT legacy AS fixed FROM users'
        ),
        # qb_w
        (
            BaseTest.qb_w.select(Column('name')).from_table('users'),
            'SELECT "name" FROM "users"'
        ),
        (
            BaseTest.qb_w.select(Column('legacy').as_('fixed')).from_table('users'),
            'SELECT "legacy" AS "fixed" FROM "users"'
        ),
    ])
    def test_column(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.select(Parameter('name')).from_table('users'),
            'SELECT %(p1)s FROM users',
            {'p1': 'name'}
        ),
        (
            BaseTest.qb.select(Parameter('name').as_('alias')).from_table('users'),
            'SELECT %(p1)s AS alias FROM users',
            {'p1': 'name'}
        )
    ])
    def test_parameter(self, query: QueryProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

    @parameterized.expand([
        (
            BaseTest.qb.select(Value('name')).from_table('users'),
            "SELECT 'name' FROM users",
        ),
        (
            BaseTest.qb_w.select(Value('name').as_('alias')).from_table('users'),
            'SELECT \'name\' AS "alias" FROM "users"',
        ),
        (
            BaseTest.qb.select(Value(1)).from_table('users'),
            "SELECT 1 FROM users",
        ),
        (
            BaseTest.qb_w.select(Value(1).as_('alias')).from_table('users'),
            'SELECT 1 AS "alias" FROM "users"',
        ),
        (
            BaseTest.qb.select(Value(0.69)).from_table('users'),
            "SELECT 0.69 FROM users",
        ),
        (
            BaseTest.qb_w.select(Value(0.96).as_('alias')).from_table('users'),
            'SELECT 0.96 AS "alias" FROM "users"',
        )
    ])
    def test_value(self, query: QueryProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
