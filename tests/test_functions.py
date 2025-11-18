from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.expressions import param, val
from david8.functions import avg, concat, count, max_, min_, sum_
from david8.logical_operators import and_, or_, xor
from david8.predicates import eq_e
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
            .having(eq_e(count('*'), val(1)))
        )

        for expr in [
            eq_e(count('name'), val(2)),
            eq_e(max_('price'), val(1000)),
            eq_e(min_('age'), val(27)),
            eq_e(sum_('money'), val(100)),
            eq_e(avg('success'), val(99)),
            eq_e(count('name', True), val(3)),
            eq_e(max_('price', True), val(2000)),
            eq_e(min_('age', True), val(33)),
            eq_e(sum_('money', True), val(200)),
            eq_e(avg('success', True), val(299)),
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
                    eq_e(count('name'), val(2)),
                    eq_e(max_('price'), val(1000)),
                    and_(
                        eq_e(min_('age'), val(27)),
                        eq_e(sum_('money'), val(100)),
                    ),
                    xor(
                        eq_e(avg('success'), val(99)),
                        eq_e(avg('happiness'), val(101)),
                    )
                )
            )
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM test HAVING (count(name) = 2 OR max(price) = 1000 OR (min(age) = 27 '
            'AND sum(money) = 100) OR (avg(success) = 99 XOR avg(happiness) = 101))'
        )
