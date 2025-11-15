from parameterized import parameterized

from david8 import QueryBuilderProtocol, get_qb
from david8.dialects import ClickhouseDialect
from david8.expressions import Column, Parameter, as_
from david8.functions import concat
from tests.base_test import BaseTest


class TestFunctions(BaseTest):

    @parameterized.expand([
        (
            get_qb(ClickhouseDialect()),
            "SELECT concat('static-value1', col1, %(p1)s, '1', '1.5', "
            "concat('static-value2', col2, %(p2)s, '2', '2.5')), concat(col3, %(p3)s, "
            "'static-value3') AS alias FROM test",
        ),
        (
            get_qb(ClickhouseDialect(True)),
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
                    Column('col1'),
                    Parameter('value1'),
                    1,
                    1.5,
                    concat(
                        'static-value2',
                        Column('col2'),
                        Parameter('value2'),
                        2,
                        2.5,
                    ),
                ),
                as_(
                    concat(Column('col3'), Parameter('value3'), 'static-value3'),
                    'alias'
                ),
            )
            .from_table('test')
        )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'value1', 'p2': 'value2', 'p3': 'value3'}, query.get_parameters())
