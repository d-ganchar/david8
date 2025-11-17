from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.expressions import col, param
from david8.functions import concat
from tests.base_test import BaseTest


class TestFunctions(BaseTest):

    @parameterized.expand([
        (
            BaseTest.qb,
            "SELECT concat('static-value1', col1, %(p1)s, '1', '1.5', "
            "concat('static-value2', col2, %(p2)s, '2', '2.5')), concat(col3, %(p3)s, "
            "'static-value3') AS alias FROM test",
        ),
        (
            BaseTest.qb_w,
            'SELECT concat(\'static-value1\', "col1", %(p1)s, \'1\', \'1.5\', '
            'concat(\'static-value2\', "col2", %(p2)s, \'2\', \'2.5\')), concat("col3", '
            '%(p3)s, \'static-value3\') AS "alias" FROM "test"'
        )
    ])
    def test_concat(self, qb: QueryBuilderProtocol, exp_sql: str):
        query = (
            qb
            .select(
                concat(
                    'static-value1',
                    col('col1'),
                    param('value1'),
                    1,
                    1.5,
                    concat(
                        'static-value2',
                        col('col2'),
                        param('value2'),
                        2,
                        2.5,
                    ),
                ),
                concat(col('col3'), param('value3'), 'static-value3').as_('alias')
            )
            .from_table('test')
        )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'value1', 'p2': 'value2', 'p3': 'value3'}, query.get_parameters())
