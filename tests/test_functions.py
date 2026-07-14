from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.cast_types import bigint, char, date_, integer, smallint, text, time_, timestamp_, varchar
from david8.expressions import desc
from david8.expressions import param as p
from david8.expressions import val as v
from david8.frames import current_row, following, preceding, range_, rows, unbounded_following, unbounded_preceding
from david8.functions import (
    add,
    avg,
    cast,
    concat,
    corr,
    count,
    covar_pop,
    covar_samp,
    cume_dist,
    div,
    first_value,
    generate_series,
    greatest,
    lag,
    lead,
    least,
    length,
    lower,
    max_,
    min_,
    mul,
    now_,
    nth_value,
    null_if,
    percent_rank,
    position,
    rank,
    regr_avgx,
    regr_count,
    regr_intercept,
    regr_r2,
    regr_slope,
    regr_sxx,
    regr_syy,
    replace_,
    round_,
    stddev_pop,
    stddev_samp,
    sub,
    substring,
    sum_,
    trim,
    upper,
    uuid_,
    var_pop,
    var_samp,
)
from david8.logical_operators import and_, or_, xor
from david8.predicates import eq
from david8.protocols.sql import AggFunctionProtocol, FunctionProtocol
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
                    v('val1'),
                    p('param1'),
                    1,
                    1.5,
                    concat(
                        'col_name2',
                        v('val2'),
                        p('param2'),
                        2,
                        2.5,
                    ),
                ),
                concat('col3', p('param3'), 'col_name3').as_('alias')
            )
            .from_table('test')
        )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'param1', 'p2': 'param2', 'p3': 'param3'}, query.get_parameters())

    def test_round(self):
        self.assertEqual(
            self.qb.select(round_('col1', 2)).get_sql(),
            'SELECT round(col1, 2)'
        )

    @parameterized.expand([
        (
            greatest('col1', 'col2', 'col3'),
            'SELECT greatest(col1, col2, col3)',
            {}
        ),
        (
            greatest(1, p(25), 'col'),
            'SELECT greatest(1, %(p1)s, col)',
            {'p1': 25}
        ),
    ])
    def test_greatest(self, fn: FunctionProtocol, sql_exp: str, params: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), sql_exp)
        self.assertEqual(query.get_parameters(), params)


    @parameterized.expand([
        (
            least('col1', 'col2', 'col3'),
            'SELECT least(col1, col2, col3)',
            {}
        ),
        (
            least(1, p(25), 'col'),
            'SELECT least(1, %(p1)s, col)',
            {'p1': 25}
        ),
    ])
    def test_least(self, fn: FunctionProtocol, sql_exp: str, params: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), sql_exp)
        self.assertEqual(query.get_parameters(), params)


class TestAggFunctions(BaseTest):

    def test_agg_functions(self):
        query = (
            self.qb
            .select('*')
            .from_table('test')
            .having(eq(count('*'), v(1)))
        )

        for expr in [
            eq(count('name'), v(2)),
            eq(max_('price'), v(1000)),
            eq(min_('age'), v(27)),
            eq(sum_('money'), v(100)),
            eq(avg('success'), v(99)),
            eq(count('name', True), v(3)),
            eq(max_('price', True), v(2000)),
            eq(min_('age', True), v(33)),
            eq(sum_('money', True), v(200)),
            eq(avg('success', True), v(299)),
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
                    eq(count('name'), v(2)),
                    eq(max_('price'), v(1000)),
                    and_(
                        eq(min_('age'), v(27)),
                        eq(sum_('money'), v(100)),
                    ),
                    xor(
                        eq(avg('success'), v(99)),
                        eq(avg('happiness'), v(101)),
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
            length(v('MyVAR')),
            "SELECT length('MyVAR')",
            "SELECT length('MyVAR')",
            {},
        ),
        (
            length(p('myParam')),
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
            upper(v('MyVAR')),
            "SELECT upper('MyVAR')",
            "SELECT upper('MyVAR')",
            {},
        ),
        (
            upper(p('myParam')),
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
            lower(v('MyVAR')),
            "SELECT lower('MyVAR')",
            "SELECT lower('MyVAR')",
            {},
        ),
        (
            lower(p('myParam')),
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
            trim(v('MyVAR')),
            "SELECT trim('MyVAR')",
            "SELECT trim('MyVAR')",
            {},
        ),
        (
            trim(p('myParam')),
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
            cast(v('1'), smallint).as_('small_int_val'),
            "SELECT CAST('1' AS SMALLINT) AS small_int_val",
        ),
        (
            cast(v('2025-11-27 15:54:34.173122+00'), timestamp_),
            "SELECT CAST('2025-11-27 15:54:34.173122+00' AS TIMESTAMP)",
        ),
        (
            cast(v('2025-11-27 15:54:34.173122+00'), date_),
            "SELECT CAST('2025-11-27 15:54:34.173122+00' AS DATE)",
        ),
        (
            cast(v('2025-11-27 15:54:34.173122+00'), time_),
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
            replace_('col_name', 'Saruman', p('Gandalf')),
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
            substring('col_name', 1, p(3)),
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
            position('col_name', p('Matrix')),
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

    @parameterized.expand([
        (
            null_if('col_name', 'unknown'),
            "SELECT nullif(col_name, 'unknown')",
        ),
        (
            null_if('int_col', 65).as_('number'),
            'SELECT nullif(int_col, 65) AS number',
        ),
        (
            null_if('col_name', 0.9),
            'SELECT nullif(col_name, 0.9)',
        ),
    ])
    def test_null_if(self, fn: FunctionProtocol, sql_exp: str):
        self.assertEqual(self.qb.select(fn).get_sql(), sql_exp)

    @parameterized.expand([
        # partition_by
        (
            sum_('salary').over(['dept']).as_('by_dept'),
            'SELECT sum(salary) OVER (PARTITION BY dept) AS by_dept',
        ),
        (
            avg('salary').over(['dept']).as_('by_dept'),
            'SELECT avg(salary) OVER (PARTITION BY dept) AS by_dept',
        ),
        (
            max_('salary').over(['dept']).as_('by_dept'),
            'SELECT max(salary) OVER (PARTITION BY dept) AS by_dept',
        ),
        (
            min_('salary').over(['dept']).as_('by_dept'),
            'SELECT min(salary) OVER (PARTITION BY dept) AS by_dept',
        ),
        (
            sum_('salary').over([null_if('dept', 0)]).as_('by_dept'),
            'SELECT sum(salary) OVER (PARTITION BY nullif(dept, 0)) AS by_dept',
        ),
        (
            avg('salary').over([null_if('dept', 0)]).as_('by_dept'),
            'SELECT avg(salary) OVER (PARTITION BY nullif(dept, 0)) AS by_dept',
        ),
        (
            max_('salary').over([null_if('dept', 0)]).as_('by_dept'),
            'SELECT max(salary) OVER (PARTITION BY nullif(dept, 0)) AS by_dept',
        ),
        (
            min_('salary').over([null_if('dept', 0)]).as_('by_dept'),
            'SELECT min(salary) OVER (PARTITION BY nullif(dept, 0)) AS by_dept',
        ),
        # partition_by + order_by
        (
            sum_('salary').over(partition_by=['dept'], order_by=[desc('salary'), 'name']).as_('by_dept'),
            'SELECT sum(salary) OVER (PARTITION BY dept ORDER BY salary DESC, name) AS by_dept',
        ),
        (
            avg('salary').over(partition_by=['dept'], order_by=[desc('salary', 'name')]).as_('by_dept'),
            'SELECT avg(salary) OVER (PARTITION BY dept ORDER BY salary DESC, name DESC) AS by_dept',
        ),
        (
            max_('salary').over(partition_by=['dept'], order_by=[desc('name'), 'salary']).as_('by_dept'),
            'SELECT max(salary) OVER (PARTITION BY dept ORDER BY name DESC, salary) AS by_dept',
        ),
        (
            min_('salary').over(partition_by=['dept'], order_by=['salary', 'name']).as_('by_dept'),
            'SELECT min(salary) OVER (PARTITION BY dept ORDER BY salary, name) AS by_dept',
        ),
        (
            sum_('salary').over(
                partition_by=['dept'],
                order_by=[desc('salary'), 'name'],
                frame_mode=rows(unbounded_preceding())
            ).as_('by_dept'),
            'SELECT sum(salary) OVER (PARTITION BY dept ORDER BY salary DESC, name ROWS UNBOUNDED PRECEDING) '
            'AS by_dept',
        ),
        (
            avg('salary').over(
                partition_by=['dept'],
                order_by=[desc('salary', 'name')],
                frame_mode=rows(unbounded_preceding())
            ).as_('by_dept'),
            'SELECT avg(salary) OVER (PARTITION BY dept ORDER BY salary DESC, name DESC ROWS UNBOUNDED PRECEDING) '
            'AS by_dept',
        ),
        (
            max_('salary').over(
                partition_by=['dept'],
                order_by=[desc('name'), 'salary'],
                frame_mode=rows(unbounded_preceding())
            ).as_('by_dept'),
            'SELECT max(salary) OVER (PARTITION BY dept ORDER BY name DESC, salary ROWS UNBOUNDED PRECEDING) '
            'AS by_dept',
        ),
        (
            min_('salary').over(
                partition_by=['dept'],
                order_by=['salary', 'name'],
                frame_mode=rows(unbounded_preceding())
            ).as_('by_dept'),
            'SELECT min(salary) OVER (PARTITION BY dept ORDER BY salary, name ROWS UNBOUNDED PRECEDING) AS by_dept',
        ),
        (
            sum_('salary').over(
                partition_by=['dept'],
                order_by=[desc('salary'), 'name'],
                frame_mode=rows(preceding(), current_row())
            ).as_('by_dept'),
            'SELECT sum(salary) OVER (PARTITION BY dept ORDER BY salary DESC, name ROWS BETWEEN PRECEDING AND '
            'CURRENT ROW) '
            'AS by_dept',
        ),
        (
            avg('salary').over(
                partition_by=['dept'],
                order_by=[desc('salary', 'name')],
                frame_mode=range_(unbounded_following(), following())
            ).as_('by_dept'),
            'SELECT avg(salary) OVER (PARTITION BY dept ORDER BY salary DESC, name DESC RANGE BETWEEN UNBOUNDED '
            'FOLLOWING AND FOLLOWING) '
            'AS by_dept',
        ),
        (
            max_('salary').over(
                partition_by=['dept'],
                order_by=[desc('name'), 'salary'],
                frame_mode=range_(current_row())
            ).as_('by_dept'),
            'SELECT max(salary) OVER (PARTITION BY dept ORDER BY name DESC, salary RANGE CURRENT ROW) '
            'AS by_dept',
        ),
        (
            min_('salary').over(
                partition_by=['dept'],
                order_by=['salary', 'name'],
                frame_mode=rows(unbounded_preceding(), current_row())
            ).as_('by_dept'),
            'SELECT min(salary) OVER (PARTITION BY dept ORDER BY salary, name ROWS BETWEEN UNBOUNDED PRECEDING AND '
            'CURRENT ROW) AS by_dept',
        ),
    ])
    def test_unnamed_window_fn(self, fn: FunctionProtocol, sql_exp: str):
        self.assertEqual(self.qb.select(fn).get_sql(), sql_exp)

    @parameterized.expand([
        # partition_by
        (
            sum_('salary').over(['dept'], window='w_name').as_('by_dept'),
            'SELECT sum(salary) OVER (w_name PARTITION BY dept) AS by_dept',
        ),
        (
            avg('salary').over(['dept'], window='w_name').as_('by_dept'),
            'SELECT avg(salary) OVER (w_name PARTITION BY dept) AS by_dept',
        ),
        (
            max_('salary').over(['dept'], window='w_name').as_('by_dept'),
            'SELECT max(salary) OVER (w_name PARTITION BY dept) AS by_dept',
        ),
        (
            min_('salary').over(['dept'], window='w_name').as_('by_dept'),
            'SELECT min(salary) OVER (w_name PARTITION BY dept) AS by_dept',
        ),
        (
            sum_('salary').over([null_if('dept', 0)], window='w_name').as_('by_dept'),
            'SELECT sum(salary) OVER (w_name PARTITION BY nullif(dept, 0)) AS by_dept',
        ),
        (
            avg('salary').over([null_if('dept', 0)], window='w_name').as_('by_dept'),
            'SELECT avg(salary) OVER (w_name PARTITION BY nullif(dept, 0)) AS by_dept',
        ),
        (
            max_('salary').over([null_if('dept', 0)], window='w_name').as_('by_dept'),
            'SELECT max(salary) OVER (w_name PARTITION BY nullif(dept, 0)) AS by_dept',
        ),
        (
            min_('salary').over([null_if('dept', 0)], window='w_name').as_('by_dept'),
            'SELECT min(salary) OVER (w_name PARTITION BY nullif(dept, 0)) AS by_dept',
        ),
        # partition_by + order_by
        (
            sum_('salary').over(partition_by=['dept'], order_by=[desc('salary'), 'name'], window='w_name')
            .as_('by_dept'),
            'SELECT sum(salary) OVER (w_name PARTITION BY dept ORDER BY salary DESC, name) AS by_dept',
        ),
        (
            avg('salary').over(partition_by=['dept'], order_by=[desc('salary'), desc('name')], window='w_name')
            .as_('by_dept'),
            'SELECT avg(salary) OVER (w_name PARTITION BY dept ORDER BY salary DESC, name DESC) AS by_dept',
        ),
        (
            max_('salary').over(partition_by=['dept'], order_by=[desc('name'), 'salary'], window='w_name')
            .as_('by_dept'),
            'SELECT max(salary) OVER (w_name PARTITION BY dept ORDER BY name DESC, salary) AS by_dept',
        ),
        (
            min_('salary').over(partition_by=['dept'], order_by=['salary', 'name'], window='w_name')
            .as_('by_dept'),
            'SELECT min(salary) OVER (w_name PARTITION BY dept ORDER BY salary, name) AS by_dept',
        ),
        (
            sum_('salary').over(
                partition_by=['dept'],
                order_by=[desc('salary'), 'name'],
                frame_mode=rows(unbounded_preceding()),
                window='w_name'
            ).as_('by_dept'),
            'SELECT sum(salary) OVER (w_name PARTITION BY dept ORDER BY salary DESC, name ROWS UNBOUNDED PRECEDING) '
            'AS by_dept',
        ),
        (
            avg('salary').over(
                partition_by=['dept'],
                order_by=[desc('salary', 'name')],
                frame_mode=rows(unbounded_preceding()),
                window='w_name',
            ).as_('by_dept'),
            'SELECT avg(salary) OVER (w_name PARTITION BY dept ORDER BY salary DESC, name DESC ROWS UNBOUNDED '
            'PRECEDING) AS by_dept',
        ),
        (
            max_('salary').over(
                partition_by=['dept'],
                order_by=[desc('name'), 'salary'],
                frame_mode=rows(unbounded_preceding()),
                window='w_name',
            ).as_('by_dept'),
            'SELECT max(salary) OVER (w_name PARTITION BY dept ORDER BY name DESC, salary ROWS UNBOUNDED PRECEDING) '
            'AS by_dept',
        ),
        (
            min_('salary').over(
                partition_by=['dept'],
                order_by=['salary', 'name'],
                frame_mode=rows(unbounded_preceding()),
                window='w_name',
            ).as_('by_dept'),
            'SELECT min(salary) OVER (w_name PARTITION BY dept ORDER BY salary, name ROWS UNBOUNDED PRECEDING) AS '
            'by_dept',
        ),
        (
            sum_('salary').over(
                partition_by=['dept'],
                order_by=[desc('salary'), 'name'],
                frame_mode=rows(preceding(), current_row()),
                window='w_name',
            ).as_('by_dept'),
            'SELECT sum(salary) OVER (w_name PARTITION BY dept ORDER BY salary DESC, name ROWS BETWEEN PRECEDING AND '
            'CURRENT ROW) AS by_dept',
        ),
        (
            avg('salary').over(
                partition_by=['dept'],
                order_by=[desc('salary', 'name')],
                frame_mode=range_(unbounded_following(), following()),
                window='w_name',
            ).as_('by_dept'),
            'SELECT avg(salary) OVER (w_name PARTITION BY dept ORDER BY salary DESC, name DESC RANGE BETWEEN '
            'UNBOUNDED FOLLOWING AND FOLLOWING) AS by_dept',
        ),
        (
            max_('salary').over(
                partition_by=['dept'],
                order_by=[desc('name'), 'salary'],
                frame_mode=range_(current_row()),
                window='w_name',
            ).as_('by_dept'),
            'SELECT max(salary) OVER (w_name PARTITION BY dept ORDER BY name DESC, salary RANGE CURRENT ROW) '
            'AS by_dept',
        ),
        (
            min_('salary').over(
                partition_by=['dept'],
                order_by=['salary', 'name'],
                frame_mode=rows(unbounded_preceding(), current_row()),
                window='w_name',
            ).as_('by_dept'),
            'SELECT min(salary) OVER (w_name PARTITION BY dept ORDER BY salary, name ROWS BETWEEN UNBOUNDED '
            'PRECEDING AND CURRENT ROW) AS by_dept',
        ),
    ])
    def test_named_window_fn(self, fn: FunctionProtocol, sql_exp: str):
        self.assertEqual(self.qb.select(fn).get_sql(), sql_exp)

    @parameterized.expand([
        (
            var_pop('salary').over(partition_by=['dept'], order_by=['date']),
            'SELECT var_pop(salary) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            var_samp('salary').over(partition_by=['dept'], order_by=['date']),
            'SELECT var_samp(salary) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            stddev_pop('salary').over(partition_by=['dept'], order_by=['date']),
            'SELECT stddev_pop(salary) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            stddev_samp('salary').over(partition_by=['dept'], order_by=['date']),
            'SELECT stddev_samp(salary) OVER (PARTITION BY dept ORDER BY date)',
        ),
    ])
    def test_1_arg_fn(self, fn: AggFunctionProtocol, exp_sql: str):
        self.assertEqual(BaseTest.qb.select(fn).get_sql(), exp_sql)

    @parameterized.expand([
        (
            corr('salary', 'bonus').over(partition_by=['dept'], order_by=['date']),
            'SELECT corr(salary, bonus) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            covar_pop('salary', 'bonus').over(partition_by=['dept'], order_by=['date']),
            'SELECT covar_pop(salary, bonus) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_slope('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_slope(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_r2('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_r2(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_sxx('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_sxx(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_syy('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_syy(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_avgx('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_avgx(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_count('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_count(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_intercept('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_intercept(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            covar_samp('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT covar_samp(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
    ])
    def test_2_arg_fn(self, fn: AggFunctionProtocol, exp_sql: str):
        self.assertEqual(BaseTest.qb.select(fn).get_sql(), exp_sql)

    @parameterized.expand([
        (
            min_('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT min(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            max_('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT max(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            avg('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT avg(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            count('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT count(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            var_pop('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT var_pop(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            var_samp('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT var_samp(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            stddev_pop('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT stddev_pop(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            stddev_samp('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT stddev_samp(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            first_value('salary').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT first_value(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            nth_value('salary', 3).filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT nth_value(salary, 3) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            lag('salary', 3).filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT lag(salary, 3) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            lead('salary', 3).filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT lead(salary, 3) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            percent_rank().over(partition_by=['dept'], order_by=['date']),
            'SELECT percent_rank() OVER (PARTITION BY dept ORDER BY date)',
            {},
        ),
        (
            rank().over(partition_by=['dept'], order_by=['date']),
            'SELECT rank() OVER (PARTITION BY dept ORDER BY date)',
            {},
        ),
        (
            cume_dist().over(partition_by=['dept'], order_by=['date']),
            'SELECT cume_dist() OVER (PARTITION BY dept ORDER BY date)',
            {},
        ),
        (
            corr('salary', 'bonus').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT corr(salary, bonus) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            covar_pop('salary', 'bonus').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT covar_pop(salary, bonus) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            regr_slope('salary', 'experience').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_slope(salary, experience) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            regr_r2('salary', 'experience').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_r2(salary, experience) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            regr_sxx('salary', 'experience').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_sxx(salary, experience) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            regr_syy('salary', 'experience').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_syy(salary, experience) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            regr_avgx('salary', 'experience').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_avgx(salary, experience) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            regr_count('salary', 'experience').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_count(salary, experience) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            regr_intercept('salary', 'experience').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_intercept(salary, experience) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
        (
            covar_samp('salary', 'experience').filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date']),
            'SELECT covar_samp(salary, experience) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date)',
            {'p1': 'ok'},
        ),
    ])
    def test_filter(self, fn: AggFunctionProtocol, exp_sql: str, exp_params: dict):
        query = BaseTest.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)


class TestArithmeticFunctions(BaseTest):
    @parameterized.expand([
        (
            add('col1', 'col2', 'col3'),
            'SELECT (col1 + col2 + col3)',
        ),
        (
            div('col1', 'col2', 'col3'),
            'SELECT (col1 / col2 / col3)',
        ),
        (
            sub('col1', 'col2', 'col3'),
            'SELECT (col1 - col2 - col3)',
        ),
        (
            mul('col1', 'col2', 'col3'),
            'SELECT (col1 * col2 * col3)',
        ),
    ])
    def test_base_arithmetic_fn(self, fn: FunctionProtocol, sql_exp: str):
        self.assertEqual(self.qb.select(fn).get_sql(), sql_exp)
