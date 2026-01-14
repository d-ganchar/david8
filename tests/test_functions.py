from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.cast_types import bigint, char, date_, integer, smallint, text, time_, timestamp_, varchar
from david8.expressions import param, val
from david8.functions import (
    avg,
    cast,
    concat,
    count,
    generate_series,
    length,
    lower,
    max_,
    min_,
    now_,
    position,
    replace_,
    substring,
    sum_,
    trim,
    upper,
    uuid_,
)
from david8.logical_operators import and_, or_, xor
from david8.predicates import eq
from david8.protocols.sql import FunctionProtocol
from tests.base_test import BaseTest


class TestFunctions(BaseTest):

    @parameterized.expand([
        (
            BaseTest.qb,
            "SELECT concat(col_name1, 'val1', %(p1)s, '1', '1.5', concat(col_name2, "
            "'val2', %(p2)s, '2', '2.5')), concat(col3, %(p3)s, col_name3) AS alias FROM test",
        ),
        (
            BaseTest.qb_w,
            'SELECT concat("col_name1", \'val1\', %(p1)s, \'1\', \'1.5\', '
            'concat("col_name2", \'val2\', %(p2)s, \'2\', \'2.5\')), concat("col3", '
            '%(p3)s, "col_name3") AS "alias" FROM "test"'
        )
    ])
    def test_concat(self, qb: QueryBuilderProtocol, exp_sql: str):
        query = (
            qb
            .select(
                concat(
                    'col_name1',
                    val('val1'),
                    param('param1'),
                    1,
                    1.5,
                    concat(
                        'col_name2',
                        val('val2'),
                        param('param2'),
                        2,
                        2.5,
                    ),
                ),
                concat('col3', param('param3'), 'col_name3').as_('alias')
            )
            .from_table('test')
        )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'param1', 'p2': 'param2', 'p3': 'param3'}, query.get_parameters())


class TestAggFunctions(BaseTest):

    def test_agg_functions(self):
        query = (
            self.qb
            .select('*')
            .from_table('test')
            .having(eq(count('*'), val(1)))
        )

        for expr in [
            eq(count('name'), val(2)),
            eq(max_('price'), val(1000)),
            eq(min_('age'), val(27)),
            eq(sum_('money'), val(100)),
            eq(avg('success'), val(99)),
            eq(count('name', True), val(3)),
            eq(max_('price', True), val(2000)),
            eq(min_('age', True), val(33)),
            eq(sum_('money', True), val(200)),
            eq(avg('success', True), val(299)),
        ]:
            query.having(expr)

        sql = query.get_sql()
        self.assertEqual(
            sql,
            'SELECT * FROM test HAVING count(*) = 1 AND count(name) = 2 AND max(price) = 1000 AND min(age) = 27 AND '
            'sum(money) = 100 AND avg(success) = 99 AND count(DISTINCT name) = 3 AND max(DISTINCT price) = 2000 AND '
            'min(DISTINCT age) = 33 AND sum(DISTINCT money) = 200 AND avg(DISTINCT success) = 299'
        )

    def test_agg_logical_operators(self):
        query = (
            self.qb
            .select('*')
            .from_table('test')
            .having(
                or_(
                    eq(count('name'), val(2)),
                    eq(max_('price'), val(1000)),
                    and_(
                        eq(min_('age'), val(27)),
                        eq(sum_('money'), val(100)),
                    ),
                    xor(
                        eq(avg('success'), val(99)),
                        eq(avg('happiness'), val(101)),
                    )
                )
            )
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM test HAVING (count(name) = 2 OR max(price) = 1000 OR (min(age) = 27 '
            'AND sum(money) = 100) OR (avg(success) = 99 XOR avg(happiness) = 101))'
        )

    @parameterized.expand([
        # length
        (
            length(concat('col1', 'col2')),
            'SELECT length(concat(col1, col2))',
            'SELECT length(concat("col1", "col2"))',
            {},
        ),
        (
            length('col_name'),
            'SELECT length(col_name)',
            'SELECT length("col_name")',
            {},
        ),
        (
            length(val('MyVAR')),
            "SELECT length('MyVAR')",
            "SELECT length('MyVAR')",
            {},
        ),
        (
            length(param('myParam')),
            'SELECT length(%(p1)s)',
            'SELECT length(%(p1)s)',
            {'p1': 'myParam'},
        ),
        # upper
        (
            upper('col_name'),
            'SELECT upper(col_name)',
            'SELECT upper("col_name")',
            {},
        ),
        (
            upper(val('MyVAR')),
            "SELECT upper('MyVAR')",
            "SELECT upper('MyVAR')",
            {},
        ),
        (
            upper(param('myParam')),
            'SELECT upper(%(p1)s)',
            'SELECT upper(%(p1)s)',
            {'p1': 'myParam'},
        ),
        # lower
        (
            lower('col_name'),
            'SELECT lower(col_name)',
            'SELECT lower("col_name")',
            {},
        ),
        (
            lower(val('MyVAR')),
            "SELECT lower('MyVAR')",
            "SELECT lower('MyVAR')",
            {},
        ),
        (
            lower(param('myParam')),
            'SELECT lower(%(p1)s)',
            'SELECT lower(%(p1)s)',
            {'p1': 'myParam'},
        ),
        # trim
        (
            trim('col_name'),
            'SELECT trim(col_name)',
            'SELECT trim("col_name")',
            {},
        ),
        (
            trim(val('MyVAR')),
            "SELECT trim('MyVAR')",
            "SELECT trim('MyVAR')",
            {},
        ),
        (
            trim(param('myParam')),
            'SELECT trim(%(p1)s)',
            'SELECT trim(%(p1)s)',
            {'p1': 'myParam'},
        ),
    ])
    def test_str_arg_fn(self, fn: FunctionProtocol, sql_exp: str, sql_expr2: str, exp_param: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), sql_exp)
        self.assertEqual(query.get_parameters(), exp_param)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), sql_expr2)
        self.assertEqual(query.get_parameters(), exp_param)

    @parameterized.expand([
        (
            now_(),
            'SELECT now()',
        ),
        (
            uuid_(),
            'SELECT uuid()',
        ),
    ])
    def test_zero_arg_fn(self, fn: FunctionProtocol, sql_exp: str):
        self.assertEqual(self.qb.select(fn).get_sql(), sql_exp)

    @parameterized.expand([
        (
            cast('col_name', integer),
            'SELECT CAST(col_name AS INTEGER)',
        ),
        (
            cast('col_name', bigint),
            'SELECT CAST(col_name AS BIGINT)',
        ),
        (
            cast('col_name', text),
            'SELECT CAST(col_name AS TEXT)',
        ),
        (
            cast('col_name', char(9)),
            'SELECT CAST(col_name AS CHAR(9))',
        ),
        (
            cast('col_name', varchar(9)),
            'SELECT CAST(col_name AS VARCHAR(9))',
        ),
        (
            cast(val('1'), smallint).as_('small_int_val'),
            "SELECT CAST('1' AS SMALLINT) AS small_int_val",
        ),
        (
            cast(val('2025-11-27 15:54:34.173122+00'), timestamp_),
            "SELECT CAST('2025-11-27 15:54:34.173122+00' AS TIMESTAMP)",
        ),
        (
            cast(val('2025-11-27 15:54:34.173122+00'), date_),
            "SELECT CAST('2025-11-27 15:54:34.173122+00' AS DATE)",
        ),
        (
            cast(val('2025-11-27 15:54:34.173122+00'), time_),
            "SELECT CAST('2025-11-27 15:54:34.173122+00' AS TIME)",
        ),
    ])
    def test_cast(self, fn: FunctionProtocol, sql_exp: str):
        self.assertEqual(self.qb.select(fn).get_sql(), sql_exp)

    @parameterized.expand([
        (
            replace_('col_name', 'Saruman', 'Gandalf'),
            "SELECT replace(col_name, 'Saruman', 'Gandalf')",
            {},
        ),
        (
            replace_('col_name', 'Saruman', param('Gandalf')),
            "SELECT replace(col_name, 'Saruman', %(p1)s)",
            {'p1': 'Gandalf'},
        ),
    ])
    def test_replace(self, fn: FunctionProtocol, sql_exp: str, exp_param: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), sql_exp)
        self.assertEqual(query.get_parameters(), exp_param)

    @parameterized.expand([
        (
            substring('col_name', 2, 3),
            'SELECT substring(col_name, 2, 3)',
            {},
        ),
        (
            substring('col_name', 1, param(3)),
            'SELECT substring(col_name, 1, %(p1)s)',
            {'p1': 3},
        ),
    ])
    def test_substring(self, fn: FunctionProtocol, sql_exp: str, exp_param: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), sql_exp)
        self.assertEqual(query.get_parameters(), exp_param)

    @parameterized.expand([
        (
            position('col_name', 'Matrix'),
            "SELECT position(col_name IN 'Matrix')",
            {},
        ),
        (
            position('col_name', param('Matrix')),
            'SELECT position(col_name IN %(p1)s)',
            {'p1': 'Matrix'},
        ),
    ])
    def test_position(self, fn: FunctionProtocol, sql_exp: str, exp_param: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), sql_exp)
        self.assertEqual(query.get_parameters(), exp_param)

    @parameterized.expand([
        (
            generate_series(3),
            'SELECT * FROM generate_series(3)',
        ),
        (
            generate_series(3, 12),
            'SELECT * FROM generate_series(3, 12)',
        ),
        (
            generate_series(3, 12, 3),
            'SELECT * FROM generate_series(3, 12, 3)',
        ),
    ])
    def test_generate_series(self, fn: FunctionProtocol, sql_exp: str):
        query = self.qb.select('*').from_expr(fn)
        self.assertEqual(query.get_sql(), sql_exp)
