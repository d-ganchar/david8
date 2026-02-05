from parameterized import parameterized

from david8 import get_default_qb
from david8.expressions import case, col, param, val
from david8.logical_operators import or_
from david8.param_styles import (
    FormatParamStyle,
    NamedParamStyle,
    NumericParamStyle,
    PyFormatParamStyle,
    QMarkParamStyle,
)
from david8.predicates import eq
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

    @parameterized.expand([
        (
            case(
                ('col_name', -1),
                ('col_name2', -2),
                else_=1,
            ),
            'SELECT CASE WHEN col_name THEN %(p1)s WHEN col_name2 THEN %(p2)s ELSE %(p3)s END',
            {'p1': -1, 'p2': -2, 'p3': 1},
        ),
        (
            case(
                (eq('status', 'active'), 1),
                (eq('status', 'online'), 2),
                else_=0,
            ),
            'SELECT CASE WHEN status = %(p1)s THEN %(p2)s WHEN status = %(p3)s THEN %(p4)s ELSE %(p5)s END',
            {'p1': 'active', 'p2': 1, 'p3': 'online', 'p4': 2, 'p5': 0},
        ),
        (
            case(
                (
                    or_(eq('status', 'active'), eq('status', 'online')),
                    1
                ),
                (eq('status', 'blocked'), -1),
                else_=col('status_num'),
            ),
            'SELECT CASE WHEN (status = %(p1)s OR status = %(p2)s) THEN %(p3)s WHEN '
            'status = %(p4)s THEN %(p5)s ELSE status_num END',
            {'p1': 'active', 'p2': 'online', 'p3': 1, 'p4': 'blocked', 'p5': -1},
        ),
    ])
    def test_case(self, expr: case, exp_sql: str, params: dict):
        query = self.qb.select(expr)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), params)
