from parameterized import parameterized

from david8 import get_qb
from david8.dialects import (
    ClickhouseDialect,
    DuckDbDialect,
    MySQLDialect,
    PostgresDialect,
    SqliteDialect,
)
from david8.param_styles import NumericParamStyle, QMarkParamStyle, FormatParamStyle
from david8.predicates import eq_val
from tests.base_test import BaseTest


class TestDialects(BaseTest):
    @parameterized.expand([
        # pg
        (
            get_qb(PostgresDialect()),
            'SELECT name, color FROM cats WHERE age = %(p1)s AND breed = %(p2)s',
            {'p1': 3, 'p2': 'ginger'},
        ),
        (
            get_qb(PostgresDialect(True)),
            'SELECT "name", "color" FROM "cats" WHERE "age" = %(p1)s AND "breed" = %(p2)s',
            {'p1': 3, 'p2': 'ginger'},
        ),
        (
            get_qb(PostgresDialect(param_style=FormatParamStyle())),
            'SELECT name, color FROM cats WHERE age = %s AND breed = %s',
            (3, 'ginger', ),
        ),
        (
            get_qb(PostgresDialect(True, FormatParamStyle())),
            'SELECT "name", "color" FROM "cats" WHERE "age" = %s AND "breed" = %s',
            (3, 'ginger', ),
        ),
        (
            get_qb(PostgresDialect(param_style=NumericParamStyle())),
            'SELECT name, color FROM cats WHERE age = $1 AND breed = $2',
            [3, 'ginger'],
        ),
        (
            get_qb(PostgresDialect(True, NumericParamStyle())),
            'SELECT "name", "color" FROM "cats" WHERE "age" = $1 AND "breed" = $2',
            [3, 'ginger'],
        ),
        # mysql
        (
            get_qb(MySQLDialect()),
            'SELECT name, color FROM cats WHERE age = %s AND breed = %s',
            (3, 'ginger',),
        ),
        (
            get_qb(MySQLDialect(True)),
            'SELECT "name", "color" FROM "cats" WHERE "age" = %s AND "breed" = %s',
            (3, 'ginger',),
        ),
        # clickhouse
        (
            get_qb(ClickhouseDialect()),
            'SELECT name, color FROM cats WHERE age = %(p1)s AND breed = %(p2)s',
            {'p1': 3, 'p2': 'ginger'},
        ),
        (
            get_qb(ClickhouseDialect(True)),
            'SELECT "name", "color" FROM "cats" WHERE "age" = %(p1)s AND "breed" = %(p2)s',
            {'p1': 3, 'p2': 'ginger'},
        ),
        # duckdb
        (
            get_qb(DuckDbDialect()),
            'SELECT name, color FROM cats WHERE age = ? AND breed = ?',
            [3, 'ginger'],
        ),
        (
            get_qb(DuckDbDialect(True)),
            'SELECT "name", "color" FROM "cats" WHERE "age" = ? AND "breed" = ?',
            [3, 'ginger'],
        ),
        # sqlite
        (
            get_qb(SqliteDialect()),
            'SELECT name, color FROM cats WHERE age = :p1 AND breed = :p2',
            {'p1': 3, 'p2': 'ginger'},
        ),
        (
            get_qb(SqliteDialect(True)),
            'SELECT "name", "color" FROM "cats" WHERE "age" = :p1 AND "breed" = :p2',
            {'p1': 3, 'p2': 'ginger'},
        ),
        (
            get_qb(SqliteDialect(param_style=QMarkParamStyle())),
            'SELECT name, color FROM cats WHERE age = ? AND breed = ?',
            [3, 'ginger']
        ),
        (
            get_qb(SqliteDialect(True, QMarkParamStyle())),
            'SELECT "name", "color" FROM "cats" WHERE "age" = ? AND "breed" = ?',
            [3, 'ginger']
        ),
    ])
    def test_dialect_format_paramstyle(self, qb, exp_sql, exp_params):
        query = (
            qb
            .select('name', 'color')
            .from_table('cats')
            .where(
                eq_val('age', 3),
                eq_val('breed', 'ginger'),
            )
         )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
