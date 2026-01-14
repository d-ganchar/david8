from parameterized import parameterized

from david8 import get_default_qb
from david8.expressions import col, param, val
from david8.param_styles import (
    FormatParamStyle,
    NamedParamStyle,
    NumericParamStyle,
    PyFormatParamStyle,
    QMarkParamStyle,
)
from david8.protocols.dialect import ParamStyleProtocol
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

    @parameterized.expand([
        (
            NumericParamStyle(),
            'SELECT $1, $2, $3',
            {'1': 'p_name', '2': 2, '3': 0.5},
            ['p_name', 2, 0.5],
        ),
        (
            QMarkParamStyle(),
            'SELECT ?, ?, ?',
            {'1': 'p_name', '2': 2, '3': 0.5},
            ['p_name', 2, 0.5],
        ),
        (
            FormatParamStyle(),
            'SELECT %s, %s, %s',
            {'1': 'p_name', '2': 2, '3': 0.5},
            ['p_name', 2, 0.5],
        ),
        (
            NamedParamStyle(),
            'SELECT :p1, :p2, :p3',
            {'p1': 'p_name', 'p2': 2, 'p3': 0.5},
            ['p_name', 2, 0.5],
        ),
        (
            PyFormatParamStyle(),
            'SELECT %(p1)s, %(p2)s, %(p3)s',
            {'p1': 'p_name', 'p2': 2, 'p3': 0.5},
            ['p_name', 2, 0.5],
        ),
    ])
    def test_param_styles(
        self,
        style: ParamStyleProtocol,
        exp_sql: str,
        exp_dict_params: dict,
        exp_list_params: list
    ):
        query = get_default_qb(style).select(param('p_name'), param(2), param(0.5))

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_dict_params)
        self.assertEqual(query.get_list_parameters(), exp_list_params)
        self.assertEqual(query.get_tuple_parameters(), tuple(exp_list_params))
